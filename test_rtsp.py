import cv2
import sys

# Test RTSP connection
rtsp_url = "rtsp://test:dei@12@12@10.7.16.48:554/stream"

print(f"Testing RTSP connection to: {rtsp_url}")
print("Attempting to connect...")

cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 10000)
cap.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, 10000)

if cap.isOpened():
    print("✓ Successfully connected to camera!")
    
    ret, frame = cap.read()
    if ret:
        print(f"✓ Successfully read frame! Frame shape: {frame.shape}")
        print("Camera is working correctly!")
    else:
        print("✗ Connected but cannot read frames")
else:
    print("✗ Cannot connect to camera")
    print("\nPossible issues:")
    print("1. Camera is not on the same network")
    print("2. RTSP URL is incorrect")
    print("3. Camera credentials are wrong")
    print("4. Firewall is blocking the connection")
    print("5. Camera RTSP service is not running")

cap.release()
