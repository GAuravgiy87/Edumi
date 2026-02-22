import cv2
import threading
import time
import logging
from typing import Optional
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import Camera, CameraPermission
from mobile_cameras.models import MobileCamera, MobileCameraPermission

logger = logging.getLogger('cameras')

def is_admin(user):
    """Check if user is admin"""
    if user.is_authenticated:
        if user.username == 'Admin' or user.username == 'admin' or user.is_superuser:
            return True
    return False

def can_manage_camera(user, camera):
    """Check if user can manage (edit/delete) a specific camera"""
    if is_admin(user):
        return True
    # Teachers can only manage cameras they have permission for
    if hasattr(user, 'userprofile') and user.userprofile.user_type == 'teacher':
        return camera.has_permission(user)
    return False

def can_view_camera(user, camera):
    """Check if user can view a specific camera"""
    if is_admin(user):
        return True
    # Teachers can view cameras they have permission for
    if hasattr(user, 'userprofile') and user.userprofile.user_type == 'teacher':
        return camera.has_permission(user)
    # Students can view all active cameras
    if hasattr(user, 'userprofile') and user.userprofile.user_type == 'student':
        return camera.is_active
    return False

def test_rtsp_paths(ip, port, username, password):
    """Test common RTSP paths to find the working one"""
    common_paths = [
        '/live',
        '/stream',
        '/h264',
        '/video',
        '/cam/realmonitor',
        '/Streaming/Channels/101',
        '/1',
        '/11',
        '/av0_0',
        '/mpeg4',
        '/media/video1',
        '/onvif1',
        '/ch0',
        '/ch01.264',
        '/',
    ]
    
    for path in common_paths:
        if username and password:
            rtsp_url = f"rtsp://{username}:{password}@{ip}:{port}{path}"
        else:
            rtsp_url = f"rtsp://{ip}:{port}{path}"
        
        try:
            cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
            cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 3000)
            cap.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, 3000)
            
            if cap.isOpened():
                ret, frame = cap.read()
                cap.release()
                
                if ret and frame is not None:
                    return path, rtsp_url
            else:
                cap.release()
        except Exception as e:
            continue
    
    return None, None

@login_required
def admin_dashboard(request):
    if not is_admin(request.user):
        return redirect('login')
    
    cameras = Camera.objects.all()
    teachers = User.objects.filter(userprofile__user_type='teacher')
    
    # Get permissions for each camera
    camera_permissions = {}
    for camera in cameras:
        camera_permissions[camera.id] = camera.get_authorized_teachers()
    
    context = {
        'cameras': cameras,
        'teachers': teachers,
        'camera_permissions': camera_permissions,
    }
    return render(request, 'cameras/admin_dashboard.html', context)

@login_required
def add_camera(request):
    if not is_admin(request.user):
        return redirect('login')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        ip_address = request.POST.get('ip_address')
        port = int(request.POST.get('port', 554))
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        # Auto-detect the correct RTSP path
        detected_path, rtsp_url = test_rtsp_paths(ip_address, port, username, password)
        
        if detected_path:
            Camera.objects.create(
                name=name,
                rtsp_url=rtsp_url,
                ip_address=ip_address,
                port=port,
                username=username,
                password=password,
                stream_path=detected_path,
                is_active=True
            )
            return redirect('admin_dashboard')
        else:
            # If auto-detection fails, save with default path
            if username and password:
                rtsp_url = f"rtsp://{username}:{password}@{ip_address}:{port}/stream"
            else:
                rtsp_url = f"rtsp://{ip_address}:{port}/stream"
            
            Camera.objects.create(
                name=name,
                rtsp_url=rtsp_url,
                ip_address=ip_address,
                port=port,
                username=username,
                password=password,
                stream_path='/stream',
                is_active=False  # Mark as inactive if path not detected
            )
            return render(request, 'cameras/add_camera.html', {
                'error': 'Could not auto-detect camera path. Camera saved but may not work. Please check camera settings.'
            })
    
    return render(request, 'cameras/add_camera.html')

@login_required
def delete_camera(request, camera_id):
    """Delete a camera and stop its streamer"""
    if not is_admin(request.user):
        return redirect('login')
    
    camera = get_object_or_404(Camera, id=camera_id)
    
    # Stop the streamer if running
    camera_manager.stop_streamer(camera_id)
    
    camera.delete()
    logger.info(f"Deleted camera {camera_id}")
    return redirect('admin_dashboard')

class CameraStreamer:
    """Non-blocking camera streamer with automatic reconnection"""
    
    def __init__(self, camera_id, rtsp_url):
        self.camera_id = camera_id
        self.rtsp_url = rtsp_url
        self.cap: Optional[cv2.VideoCapture] = None
        self.frame: Optional[bytes] = None
        self.running: bool = False
        self.thread: Optional[threading.Thread] = None
        self.lock = threading.Lock()
        self.last_access = time.time()
        self.connection_attempts = 0
        self.max_reconnect_attempts = 5
        self.reconnect_delay = 2

    def start(self):
        """Start the background streaming thread"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._update, daemon=True)
            self.thread.start()
            logger.info(f"Started streamer for camera {self.camera_id}")

    def stop(self):
        """Stop the streaming thread gracefully"""
        self.running = False
        if self.thread is not None:
            self.thread.join(timeout=2.0)
        logger.info(f"Stopped streamer for camera {self.camera_id}")

    def _connect_camera(self):
        """Establish connection to RTSP camera with timeout settings"""
        try:
            cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
            
            # Set timeouts to prevent blocking
            cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 5000)
            cap.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, 5000)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize latency
            
            if cap.isOpened():
                # Test read to verify connection
                ret, frame = cap.read()
                if ret and frame is not None:
                    self.connection_attempts = 0
                    logger.info(f"Successfully connected to camera {self.camera_id}")
                    return cap
                else:
                    cap.release()
                    logger.warning(f"Camera {self.camera_id} opened but cannot read frames")
                    return None
            else:
                cap.release()
                logger.warning(f"Cannot open camera {self.camera_id}")
                return None
                
        except Exception as e:
            logger.error(f"Error connecting to camera {self.camera_id}: {e}")
            return None

    def _update(self):
        """Background thread that continuously reads frames from camera"""
        logger.info(f"Background thread started for camera {self.camera_id}")
        
        while self.running:
            # Auto-stop if inactive for 90 seconds
            if time.time() - self.last_access > 90:
                logger.info(f"Stopping camera {self.camera_id} due to inactivity")
                break

            # Connect or reconnect to camera
            if self.cap is None:
                if self.connection_attempts >= self.max_reconnect_attempts:
                    logger.error(f"Max reconnection attempts reached for camera {self.camera_id}")
                    time.sleep(10)  # Wait longer before trying again
                    self.connection_attempts = 0
                    continue
                
                self.connection_attempts += 1
                logger.info(f"Connecting to camera {self.camera_id} (attempt {self.connection_attempts})")
                self.cap = self._connect_camera()
                
                if self.cap is None:
                    time.sleep(self.reconnect_delay)
                    continue

            # Read frame from camera
            try:
                ret, frame = self.cap.read()
                
                if ret and frame is not None:
                    # Resize for efficient streaming
                    frame = cv2.resize(frame, (960, 540))
                    
                    # Encode to JPEG with compression
                    ret, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 75])
                    
                    if ret:
                        with self.lock:
                            self.frame = jpeg.tobytes()
                    
                    # Small delay to control frame rate (~25 FPS)
                    time.sleep(0.04)
                    
                else:
                    # Frame read failed - reconnect
                    logger.warning(f"Failed to read frame from camera {self.camera_id}, reconnecting...")
                    if self.cap is not None:
                        self.cap.release()
                    self.cap = None
                    time.sleep(self.reconnect_delay)
                    
            except Exception as e:
                logger.error(f"Error reading from camera {self.camera_id}: {e}")
                if self.cap is not None:
                    self.cap.release()
                self.cap = None
                time.sleep(self.reconnect_delay)
        
        # Cleanup
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        logger.info(f"Background thread stopped for camera {self.camera_id}")

    def get_frame(self):
        """Get the latest frame (thread-safe)"""
        self.last_access = time.time()
        with self.lock:
            return self.frame

class CameraManager:
    """Global manager for camera streamers - prevents duplicate connections"""
    
    _lock = threading.Lock()
    _streamers = {}

    @classmethod
    def get_streamer(cls, camera_id, rtsp_url):
        """Get or create a streamer for the given camera"""
        with cls._lock:
            if camera_id not in cls._streamers or not cls._streamers[camera_id].running:
                logger.info(f"Creating new streamer for camera {camera_id}")
                streamer = CameraStreamer(camera_id, rtsp_url)
                streamer.start()
                cls._streamers[camera_id] = streamer
            return cls._streamers[camera_id]
    
    @classmethod
    def stop_streamer(cls, camera_id):
        """Stop a specific camera streamer"""
        with cls._lock:
            if camera_id in cls._streamers:
                cls._streamers[camera_id].stop()
                del cls._streamers[camera_id]
                logger.info(f"Removed streamer for camera {camera_id}")
    
    @classmethod
    def stop_all(cls):
        """Stop all camera streamers"""
        with cls._lock:
            for streamer in cls._streamers.values():
                streamer.stop()
            cls._streamers.clear()
            logger.info("All camera streamers stopped")

# Global manager instance
camera_manager = CameraManager()

@login_required
def camera_feed(request, camera_id):
    """Proxy camera feed from camera service on port 8001"""
    camera = get_object_or_404(Camera, id=camera_id)
    
    # Check permission
    if not can_view_camera(request.user, camera):
        return JsonResponse({'error': 'You do not have permission to view this camera'}, status=403)
    
    import requests
    
    def generate_frames():
        """Proxy frames from camera service"""
        try:
            camera_service_url = f'http://localhost:8001/api/cameras/{camera_id}/feed/'
            response = requests.get(camera_service_url, stream=True, timeout=30)
            
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    yield chunk
                    
        except requests.exceptions.RequestException as e:
            logger.error(f"Error proxying camera {camera_id}: {e}")
        except GeneratorExit:
            logger.info(f"Client disconnected from camera {camera_id}")

    response = StreamingHttpResponse(
        generate_frames(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response

@login_required
def live_monitor(request):
    """View to see all live camera feeds in a grid"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Filter RTSP cameras based on user permissions
    if is_admin(request.user):
        cameras = Camera.objects.filter(is_active=True)
        mobile_cameras = MobileCamera.objects.filter(is_active=True)
    elif hasattr(request.user, 'userprofile'):
        if request.user.userprofile.user_type == 'teacher':
            # Teachers see cameras they have permission for
            camera_ids = CameraPermission.objects.filter(teacher=request.user).values_list('camera_id', flat=True)
            cameras = Camera.objects.filter(id__in=camera_ids, is_active=True)
            
            mobile_camera_ids = MobileCameraPermission.objects.filter(teacher=request.user).values_list('mobile_camera_id', flat=True)
            mobile_cameras = MobileCamera.objects.filter(id__in=mobile_camera_ids, is_active=True)
        elif request.user.userprofile.user_type == 'student':
            # Students see all active cameras
            cameras = Camera.objects.filter(is_active=True)
            mobile_cameras = MobileCamera.objects.filter(is_active=True)
        else:
            cameras = Camera.objects.none()
            mobile_cameras = MobileCamera.objects.none()
    else:
        cameras = Camera.objects.none()
        mobile_cameras = MobileCamera.objects.none()
    
    context = {
        'cameras': cameras,
        'mobile_cameras': mobile_cameras,
    }
    return render(request, 'cameras/live_monitor.html', context)

@login_required
def view_camera(request, camera_id):
    camera = get_object_or_404(Camera, id=camera_id)
    
    # Check permission
    if not can_view_camera(request.user, camera):
        return redirect('login')
    
    return render(request, 'cameras/view_camera.html', {'camera': camera})

@login_required
def test_camera(request, camera_id):
    """Test camera via camera service"""
    if not is_admin(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    camera = get_object_or_404(Camera, id=camera_id)
    
    try:
        import requests
        camera_service_url = f'http://localhost:8001/api/cameras/{camera_id}/test/'
        response = requests.get(camera_service_url, timeout=10)
        result = response.json()
        
        # Update camera status based on test result
        if result.get('status') == 'success':
            camera.is_active = True
        else:
            camera.is_active = False
        camera.save()
        
        return JsonResponse(result)
    except Exception as e:
        logger.error(f"Error testing camera {camera_id}: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
def grant_permission(request, camera_id):
    """Grant camera access to a teacher"""
    if not is_admin(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        camera = get_object_or_404(Camera, id=camera_id)
        teacher_id = request.POST.get('teacher_id')
        teacher = get_object_or_404(User, id=teacher_id)
        
        # Verify teacher has teacher profile
        if not hasattr(teacher, 'userprofile') or teacher.userprofile.user_type != 'teacher':
            return JsonResponse({'error': 'User is not a teacher'}, status=400)
        
        # Create or get permission
        permission, created = CameraPermission.objects.get_or_create(
            camera=camera,
            teacher=teacher,
            defaults={'granted_by': request.user}
        )
        
        if created:
            return JsonResponse({'success': True, 'message': f'Access granted to {teacher.username}'})
        else:
            return JsonResponse({'success': False, 'message': 'Permission already exists'})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def revoke_permission(request, camera_id, teacher_id):
    """Revoke camera access from a teacher"""
    if not is_admin(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    camera = get_object_or_404(Camera, id=camera_id)
    teacher = get_object_or_404(User, id=teacher_id)
    
    # Delete permission
    deleted_count = CameraPermission.objects.filter(camera=camera, teacher=teacher).delete()[0]
    
    if deleted_count > 0:
        return JsonResponse({'success': True, 'message': f'Access revoked from {teacher.username}'})
    else:
        return JsonResponse({'success': False, 'message': 'Permission not found'})

@login_required
def manage_permissions(request, camera_id):
    """View to manage permissions for a specific camera"""
    if not is_admin(request.user):
        return redirect('login')
    
    camera = get_object_or_404(Camera, id=camera_id)
    all_teachers = User.objects.filter(userprofile__user_type='teacher')
    authorized_teachers = camera.get_authorized_teachers()
    unauthorized_teachers = all_teachers.exclude(id__in=authorized_teachers.values_list('id', flat=True))
    
    context = {
        'camera': camera,
        'authorized_teachers': authorized_teachers,
        'unauthorized_teachers': unauthorized_teachers,
    }
    return render(request, 'cameras/manage_permissions.html', context)

