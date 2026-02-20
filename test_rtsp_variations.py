import cv2

# Try different URL variations
urls_to_test = [
    "rtsp://test:dei@12@12@10.7.16.48:554/stream",
    "rtsp://test:dei%4012%4012@10.7.16.48:554/stream",
    "rtsp://10.7.16.48:554/stream",
    "rtsp://test:dei@12@12@10.7.16.48/stream",
    "rtsp://test:dei@12@12@10.7.16.48:554/",
    "rtsp://test:dei@12@12@10.7.16.48:554",
]

print("Testing different RTSP URL formats...\n")

for url in urls_to_test:
    print(f"Testing: {url}")
    cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 5000)
    
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"  ✓ SUCCESS! This URL works!\n")
            cap.release()
            break
        else:
            print(f"  ⚠ Connected but cannot read frames\n")
    else:
        print(f"  ✗ Cannot connect\n")
    
    cap.release()

print("\nNote: If none work, the camera might not be accessible from this network.")
