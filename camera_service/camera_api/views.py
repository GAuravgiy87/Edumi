"""Camera streaming views - isolated service"""
import cv2
import threading
import time
import logging
from typing import Optional
from django.http import StreamingHttpResponse, JsonResponse
import sys
from pathlib import Path

# Import Camera model from main project
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from cameras.models import Camera

logger = logging.getLogger('camera_api')

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
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._update, daemon=True)
            self.thread.start()
            logger.info(f"Started streamer for camera {self.camera_id}")

    def stop(self):
        self.running = False
        if self.thread is not None:
            self.thread.join(timeout=2.0)
        logger.info(f"Stopped streamer for camera {self.camera_id}")

    def _connect_camera(self):
        try:
            cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
            cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 5000)
            cap.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, 5000)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    self.connection_attempts = 0
                    logger.info(f"Connected to camera {self.camera_id}")
                    return cap
                cap.release()
            return None
        except Exception as e:
            logger.error(f"Error connecting camera {self.camera_id}: {e}")
            return None

    def _update(self):
        while self.running:
            if time.time() - self.last_access > 90:
                logger.info(f"Stopping camera {self.camera_id} due to inactivity")
                break

            if self.cap is None:
                if self.connection_attempts >= self.max_reconnect_attempts:
                    time.sleep(10)
                    self.connection_attempts = 0
                    continue
                
                self.connection_attempts += 1
                self.cap = self._connect_camera()
                if self.cap is None:
                    time.sleep(self.reconnect_delay)
                    continue

            try:
                ret, frame = self.cap.read()
                if ret and frame is not None:
                    # Aggressive resize for performance
                    frame = cv2.resize(frame, (640, 360), interpolation=cv2.INTER_NEAREST)
                    
                    # Lower quality encoding
                    ret, jpeg = cv2.imencode('.jpg', frame, [
                        cv2.IMWRITE_JPEG_QUALITY, 60,
                        cv2.IMWRITE_JPEG_OPTIMIZE, 1
                    ])
                    
                    if ret:
                        with self.lock:
                            self.frame = jpeg.tobytes()
                    
                    # Lower frame rate
                    time.sleep(0.05)  # ~20 FPS
                else:
                    if self.cap is not None:
                        self.cap.release()
                    self.cap = None
                    time.sleep(self.reconnect_delay)
            except Exception as e:
                logger.error(f"Error reading camera {self.camera_id}: {e}")
                if self.cap is not None:
                    self.cap.release()
                self.cap = None
                time.sleep(self.reconnect_delay)
        
        if self.cap is not None:
            self.cap.release()

    def get_frame(self):
        self.last_access = time.time()
        with self.lock:
            return self.frame

class CameraManager:
    _lock = threading.Lock()
    _streamers = {}

    @classmethod
    def get_streamer(cls, camera_id, rtsp_url):
        with cls._lock:
            if camera_id not in cls._streamers or not cls._streamers[camera_id].running:
                streamer = CameraStreamer(camera_id, rtsp_url)
                streamer.start()
                cls._streamers[camera_id] = streamer
            return cls._streamers[camera_id]
    
    @classmethod
    def stop_streamer(cls, camera_id):
        with cls._lock:
            if camera_id in cls._streamers:
                cls._streamers[camera_id].stop()
                del cls._streamers[camera_id]

camera_manager = CameraManager()

def list_cameras(request):
    """List all active cameras"""
    try:
        cameras = Camera.objects.filter(is_active=True).values('id', 'name', 'is_active')
        return JsonResponse({'cameras': list(cameras)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def camera_feed(request, camera_id):
    """Stream camera feed with aggressive optimization"""
    try:
        camera = Camera.objects.get(id=camera_id)
        streamer = camera_manager.get_streamer(camera.id, camera.rtsp_url)
        
        def generate_frames():
            frame_count = 0
            try:
                while True:
                    frame = streamer.get_frame()
                    if frame:
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n'
                               b'Content-Length: ' + str(len(frame)).encode() + b'\r\n'
                               b'\r\n' + frame + b'\r\n')
                        
                        # Skip frames for better performance
                        frame_count += 1
                        if frame_count % 3 == 0:  # Send every 3rd frame
                            time.sleep(0.05)
                        else:
                            time.sleep(0.001)
                    else:
                        time.sleep(0.1)
            except GeneratorExit:
                logger.info(f"Client disconnected from camera {camera_id}")

        response = StreamingHttpResponse(
            generate_frames(),
            content_type='multipart/x-mixed-replace; boundary=frame'
        )
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        response['X-Accel-Buffering'] = 'no'
        return response
    except Camera.DoesNotExist:
        return JsonResponse({'error': 'Camera not found'}, status=404)

def test_camera(request, camera_id):
    """Test camera connection"""
    try:
        camera = Camera.objects.get(id=camera_id)
        cap = cv2.VideoCapture(camera.rtsp_url, cv2.CAP_FFMPEG)
        cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 5000)
        
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret and frame is not None:
                return JsonResponse({'status': 'success', 'message': 'Camera accessible'})
            return JsonResponse({'status': 'error', 'message': 'Cannot read frames'})
        cap.release()
        return JsonResponse({'status': 'error', 'message': 'Cannot connect'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})



# Mobile Camera Support
import requests
import numpy as np


class MobileCameraStreamer:
    """HTTP/MJPEG streamer for mobile cameras"""
    
    def __init__(self, mobile_camera_id, stream_url):
        self.mobile_camera_id = mobile_camera_id
        self.stream_url = stream_url
        self.frame: Optional[bytes] = None
        self.running: bool = False
        self.thread: Optional[threading.Thread] = None
        self.lock = threading.Lock()
        self.last_access = time.time()

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._update, daemon=True)
            self.thread.start()
            logger.info(f"Started mobile camera streamer {self.mobile_camera_id}")

    def stop(self):
        self.running = False
        if self.thread is not None:
            self.thread.join(timeout=2.0)
        logger.info(f"Stopped mobile camera streamer {self.mobile_camera_id}")

    def _update(self):
        """Background thread to fetch frames from mobile camera"""
        while self.running:
            if time.time() - self.last_access > 90:
                logger.info(f"Stopping mobile camera {self.mobile_camera_id} due to inactivity")
                break

            try:
                response = requests.get(self.stream_url, stream=True, timeout=10)
                
                if response.status_code == 200:
                    logger.info(f"Connected to mobile camera {self.mobile_camera_id}")
                    bytes_data = bytes()
                    
                    for chunk in response.iter_content(chunk_size=1024):
                        if not self.running:
                            break
                            
                        bytes_data += chunk
                        a = bytes_data.find(b'\xff\xd8')  # JPEG start
                        b = bytes_data.find(b'\xff\xd9')  # JPEG end
                        
                        if a != -1 and b != -1:
                            jpg = bytes_data[a:b+2]
                            bytes_data = bytes_data[b+2:]
                            
                            try:
                                # Decode and resize
                                img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                                if img is not None:
                                    # Resize for efficient streaming
                                    img = cv2.resize(img, (640, 360), interpolation=cv2.INTER_NEAREST)
                                    ret, jpeg = cv2.imencode('.jpg', img, [
                                        cv2.IMWRITE_JPEG_QUALITY, 60,
                                        cv2.IMWRITE_JPEG_OPTIMIZE, 1
                                    ])
                                    if ret:
                                        with self.lock:
                                            self.frame = jpeg.tobytes()
                            except Exception as e:
                                logger.error(f"Error processing frame: {e}")
                                continue
                else:
                    logger.error(f"HTTP {response.status_code} from mobile camera {self.mobile_camera_id}")
                    time.sleep(5)
                    
            except Exception as e:
                logger.error(f"Error streaming mobile camera {self.mobile_camera_id}: {e}")
                time.sleep(5)

    def get_frame(self):
        self.last_access = time.time()
        with self.lock:
            return self.frame


class MobileCameraManager:
    _lock = threading.Lock()
    _streamers = {}

    @classmethod
    def get_streamer(cls, mobile_camera_id, stream_url):
        with cls._lock:
            if mobile_camera_id not in cls._streamers or not cls._streamers[mobile_camera_id].running:
                streamer = MobileCameraStreamer(mobile_camera_id, stream_url)
                streamer.start()
                cls._streamers[mobile_camera_id] = streamer
            return cls._streamers[mobile_camera_id]
    
    @classmethod
    def stop_streamer(cls, mobile_camera_id):
        with cls._lock:
            if mobile_camera_id in cls._streamers:
                cls._streamers[mobile_camera_id].stop()
                del cls._streamers[mobile_camera_id]


mobile_camera_manager = MobileCameraManager()


def mobile_camera_feed(request, mobile_camera_id):
    """Stream mobile camera feed"""
    from mobile_cameras.models import MobileCamera
    
    try:
        mobile_camera = MobileCamera.objects.get(id=mobile_camera_id)
        stream_url = mobile_camera.get_stream_url()
        streamer = mobile_camera_manager.get_streamer(mobile_camera.id, stream_url)
        
        def generate_frames():
            frame_count = 0
            try:
                while True:
                    frame = streamer.get_frame()
                    if frame:
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n'
                               b'Content-Length: ' + str(len(frame)).encode() + b'\r\n'
                               b'\r\n' + frame + b'\r\n')
                        
                        frame_count += 1
                        if frame_count % 2 == 0:  # Send every 2nd frame
                            time.sleep(0.05)
                        else:
                            time.sleep(0.001)
                    else:
                        time.sleep(0.1)
            except GeneratorExit:
                logger.info(f"Client disconnected from mobile camera {mobile_camera_id}")

        response = StreamingHttpResponse(
            generate_frames(),
            content_type='multipart/x-mixed-replace; boundary=frame'
        )
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        response['X-Accel-Buffering'] = 'no'
        return response
    except Exception as e:
        logger.error(f"Error in mobile_camera_feed: {e}")
        return JsonResponse({'error': str(e)}, status=500)


def test_mobile_camera(request, mobile_camera_id):
    """Test mobile camera connection"""
    from mobile_cameras.models import MobileCamera
    
    try:
        mobile_camera = MobileCamera.objects.get(id=mobile_camera_id)
        stream_url = mobile_camera.get_stream_url()
        
        response = requests.get(stream_url, timeout=5)
        
        if response.status_code == 200:
            return JsonResponse({
                'status': 'success',
                'message': 'Mobile camera accessible',
                'url': stream_url
            })
        return JsonResponse({
            'status': 'error',
            'message': f'HTTP {response.status_code}'
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
