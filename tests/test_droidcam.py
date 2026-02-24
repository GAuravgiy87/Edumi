"""
Test script to verify DroidCam connection
Run with: python test_droidcam.py
"""

import requests
import cv2
import numpy as np

# DroidCam settings
IP = "192.168.29.220"
PORT = 4747

# Common DroidCam paths
PATHS = [
    "/mjpegfeed",
    "/video",
    "/mjpeg",
    "/cam_1.mjpg",
]

print("=" * 60)
print("DroidCam Connection Test")
print("=" * 60)
print(f"IP: {IP}")
print(f"Port: {PORT}")
print()

# Test each path
for path in PATHS:
    url = f"http://{IP}:{PORT}{path}"
    print(f"Testing: {url}")
    
    try:
        response = requests.get(url, timeout=5, stream=True)
        print(f"  Status: {response.status_code}")
        print(f"  Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
        
        if response.status_code == 200:
            print(f"  ✓ SUCCESS! This path works!")
            print(f"  Full URL: {url}")
            
            # Try to read a frame
            print("  Testing frame capture...")
            bytes_data = bytes()
            for chunk in response.iter_content(chunk_size=1024):
                bytes_data += chunk
                a = bytes_data.find(b'\xff\xd8')  # JPEG start
                b = bytes_data.find(b'\xff\xd9')  # JPEG end
                
                if a != -1 and b != -1:
                    jpg = bytes_data[a:b+2]
                    img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    if img is not None:
                        print(f"  ✓ Frame captured successfully!")
                        print(f"  Frame size: {img.shape}")
                        print()
                        print("=" * 60)
                        print("RECOMMENDED SETTINGS FOR EDUMI:")
                        print("=" * 60)
                        print(f"Camera Type: DroidCam")
                        print(f"IP Address: {IP}")
                        print(f"Port: {PORT}")
                        print(f"Stream Path: {path}")
                        print("=" * 60)
                        break
            break
        else:
            print(f"  ✗ Failed")
            
    except requests.exceptions.Timeout:
        print(f"  ✗ Timeout - Cannot connect")
    except requests.exceptions.ConnectionError:
        print(f"  ✗ Connection Error - Check if DroidCam is running")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    print()

print()
print("=" * 60)
print("TROUBLESHOOTING:")
print("=" * 60)
print("1. Ensure DroidCam app is running on your phone")
print("2. Check that phone and computer are on same WiFi")
print("3. Verify the IP address shown in DroidCam app")
print("4. Try accessing http://192.168.29.220:4747 in your browser")
print("5. Check firewall settings")
print("=" * 60)
