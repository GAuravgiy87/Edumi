import cv2
import sys

# Common RTSP paths for different camera brands
common_paths = [
    "/",
    "/stream",
    "/live",
    "/h264",
    "/video",
    "/cam/realmonitor",
    "/cam/realmonitor?channel=1&subtype=0",
    "/Streaming/Channels/101",
    "/Streaming/Channels/1",
    "/videoMain",
    "/video1",
    "/live/ch00_0",
    "/live/ch0",
    "/av0_0",
    "/mpeg4",
    "/mjpeg",
    "/onvif1",
    "/onvif2",
    "/media/video1",
    "/axis-media/media.amp",
]

ip = "10.7.16.48"
port = "554"
username = "test"
password = "dei@12@12"

print("=" * 60)
print("RTSP Camera Path Finder")
print("=" * 60)
print(f"\nCamera IP: {ip}")
print(f"Port: {port}")
print(f"Username: {username}")
print(f"Password: {'*' * len(password)}")
print("\nTesting common RTSP paths...\n")

working_urls = []

for path in common_paths:
    # Try with credentials
    url_with_creds = f"rtsp://{username}:{password}@{ip}:{port}{path}"
    # Try without credentials
    url_no_creds = f"rtsp://{ip}:{port}{path}"
    
    print(f"Testing: {path}")
    
    # Test with credentials first
    cap = cv2.VideoCapture(url_with_creds, cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 3000)
    cap.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, 3000)
    
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"  ✓ SUCCESS WITH CREDENTIALS!")
            print(f"  Working URL: {url_with_creds}")
            working_urls.append(url_with_creds)
            cap.release()
            continue
    cap.release()
    
    # Test without credentials
    cap = cv2.VideoCapture(url_no_creds, cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 3000)
    cap.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, 3000)
    
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"  ✓ SUCCESS WITHOUT CREDENTIALS!")
            print(f"  Working URL: {url_no_creds}")
            working_urls.append(url_no_creds)
            cap.release()
            continue
    cap.release()
    
    print(f"  ✗ Failed")

print("\n" + "=" * 60)
if working_urls:
    print("WORKING URLS FOUND:")
    print("=" * 60)
    for url in working_urls:
        print(f"  {url}")
    print("\nUse one of these URLs in your Django admin panel!")
else:
    print("NO WORKING URLS FOUND")
    print("=" * 60)
    print("\nPossible reasons:")
    print("1. Camera is not accessible from this computer")
    print("2. Camera is on a different network")
    print("3. Firewall is blocking RTSP port 554")
    print("4. Camera credentials are incorrect")
    print("5. Camera RTSP service is disabled")
    print("\nTroubleshooting steps:")
    print("1. Ping the camera: ping 10.7.16.48")
    print("2. Check if port 554 is open: telnet 10.7.16.48 554")
    print("3. Try accessing camera web interface: http://10.7.16.48")
    print("4. Check camera manual for correct RTSP URL format")
    print("5. Try VLC Media Player: Media > Open Network Stream")
