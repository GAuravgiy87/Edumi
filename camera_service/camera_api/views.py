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
                    frame = cv2.resize(frame, (960, 540))
                    ret, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 75])
                    if ret:
                        with self.lock:
                            self.frame = jpeg.tobytes()
                    time.sleep(0.04)
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
    """Stream camera feed"""
    try:
        camera = Camera.objects.get(id=camera_id)
        streamer = camera_manager.get_streamer(camera.id, camera.rtsp_url)
        
        def generate_frames():
            try:
                while True:
                    frame = streamer.get_frame()
                    if frame:
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                        time.sleep(0.04)
                    else:
                        time.sleep(0.1)
            except GeneratorExit:
                logger.info(f"Client disconnected from camera {camera_id}")

        response = StreamingHttpResponse(
            generate_frames(),
            content_type='multipart/x-mixed-replace; boundary=frame'
        )
        response['Cache-Control'] = 'no-cache'
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
