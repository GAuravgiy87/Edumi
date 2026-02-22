"""Test DroidCam video feed"""
import requests
import cv2
import numpy as np

ip = "192.168.29.220"
port = 4747

# Test different paths
paths = ["/video", "/mjpegfeed", "/video.mjpeg", "/videofeed"]

print("Testing DroidCam video feed paths...")
print(f"IP: {ip}:{port}\n")

for path in paths:
    url = f"http://{ip}:{port}{path}"
    print(f"Testing: {url}")
    try:
        response = requests.get(url, stream=True, timeout=5)
        print(f"  Status: {response.status_code}")
        print(f"  Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
        
        if response.status_code == 200:
            # Try to read some data
            chunk = next(response.iter_content(chunk_size=1024))
            print(f"  Data received: {len(chunk)} bytes")
            
            # Check if it's MJPEG
            if b'\xff\xd8' in chunk:  # JPEG start marker
                print(f"  ✓ MJPEG stream detected!")
                print(f"  ✓✓ USE THIS PATH: {path}")
                break
            else:
                print(f"  ✗ Not MJPEG stream")
        print()
    except Exception as e:
        print(f"  Error: {e}\n")

print("\nTrying OpenCV capture...")
# Try with OpenCV
for path in ["/video", "/mjpegfeed"]:
    url = f"http://{ip}:{port}{path}"
    print(f"Testing OpenCV with: {url}")
    cap = cv2.VideoCapture(url)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret and frame is not None:
            print(f"  ✓✓ OpenCV works with {path}!")
            print(f"  Frame size: {frame.shape}")
            cap.release()
            break
        cap.release()
    print()
