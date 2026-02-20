from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse, JsonResponse, HttpResponse
from .models import Camera
import cv2
import threading
import time

def is_admin(user):
    return user.username == 'Admin' and user.is_authenticated

def is_teacher(user):
    if user.is_authenticated and hasattr(user, 'userprofile'):
        return user.userprofile.user_type == 'teacher'
    return False

def is_student(user):
    if user.is_authenticated and hasattr(user, 'userprofile'):
        return user.userprofile.user_type == 'student'
    return False

@login_required
def admin_dashboard(request):
    if not is_admin(request.user):
        return redirect('login')
    
    cameras = Camera.objects.all()
    return render(request, 'cameras/admin_dashboard.html', {'cameras': cameras})

@login_required
def add_camera(request):
    if not is_admin(request.user):
        return redirect('login')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        rtsp_url = request.POST.get('rtsp_url')
        
        Camera.objects.create(
            name=name,
            rtsp_url=rtsp_url,
            ip_address=request.POST.get('ip_address', ''),
            port=request.POST.get('port', 554),
            username=request.POST.get('username', ''),
            password=request.POST.get('password', ''),
            stream_path=request.POST.get('stream_path', '/stream')
        )
        return redirect('admin_dashboard')
    
    return render(request, 'cameras/add_camera.html')

@login_required
def delete_camera(request, camera_id):
    if not is_admin(request.user):
        return redirect('login')
    
    camera = get_object_or_404(Camera, id=camera_id)
    camera.delete()
    return redirect('admin_dashboard')

class VideoCamera:
    def __init__(self, rtsp_url):
        self.rtsp_url = rtsp_url
        self.video = None
        self.stopped = False
        
    def __del__(self):
        if self.video is not None:
            self.video.release()
    
    def get_frame(self):
        if self.video is None or not self.video.isOpened():
            # Try to open the stream with different backends
            self.video = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
            self.video.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            # Set timeout
            self.video.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 5000)
            self.video.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, 5000)
            
            if not self.video.isOpened():
                return None
        
        success, frame = self.video.read()
        if not success:
            # Try to reconnect
            self.video.release()
            self.video = None
            return None
        
        # Resize frame for better performance
        frame = cv2.resize(frame, (640, 480))
        
        # Encode frame
        ret, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        if not ret:
            return None
            
        return jpeg.tobytes()

def generate_frames(camera_url):
    """Generate frames from RTSP stream"""
    camera = VideoCamera(camera_url)
    
    while True:
        frame = camera.get_frame()
        
        if frame is None:
            # Send a placeholder or retry
            time.sleep(0.1)
            continue
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@login_required
def camera_feed(request, camera_id):
    if not is_admin(request.user):
        return redirect('login')
    
    camera = get_object_or_404(Camera, id=camera_id)
    
    try:
        return StreamingHttpResponse(
            generate_frames(camera.rtsp_url),
            content_type='multipart/x-mixed-replace; boundary=frame'
        )
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

@login_required
def view_camera(request, camera_id):
    if not is_admin(request.user):
        return redirect('login')
    
    camera = get_object_or_404(Camera, id=camera_id)
    return render(request, 'cameras/view_camera.html', {'camera': camera})

@login_required
def test_camera(request, camera_id):
    """Test if camera is accessible"""
    if not is_admin(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    camera = get_object_or_404(Camera, id=camera_id)
    
    try:
        cap = cv2.VideoCapture(camera.rtsp_url, cv2.CAP_FFMPEG)
        cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 5000)
        
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                return JsonResponse({'status': 'success', 'message': 'Camera is accessible'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Cannot read from camera'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Cannot connect to camera'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
