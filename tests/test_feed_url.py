"""Test the actual feed URL that EduMi is using"""
import requests

# Test the feed through camera service
camera_id = 5

print("Testing feed URLs...")
print("=" * 60)

# Test camera service endpoint
camera_service_url = f"http://localhost:8001/api/mobile-cameras/{camera_id}/feed/"
print(f"\n1. Camera Service Feed URL:")
print(f"   {camera_service_url}")
try:
    response = requests.get(camera_service_url, stream=True, timeout=5)
    print(f"   Status: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
    if response.status_code == 200:
        # Try to get first chunk
        chunk = next(response.iter_content(chunk_size=1024), None)
        if chunk:
            print(f"   Data received: {len(chunk)} bytes")
            print(f"   ✓ Camera service is streaming!")
        else:
            print(f"   ✗ No data received")
    else:
        print(f"   ✗ Failed: {response.text[:200]}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test main app endpoint
main_app_url = f"http://localhost:8000/mobile-cameras/feed/{camera_id}/"
print(f"\n2. Main App Feed URL:")
print(f"   {main_app_url}")
try:
    response = requests.get(main_app_url, stream=True, timeout=5)
    print(f"   Status: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
    if response.status_code == 200:
        chunk = next(response.iter_content(chunk_size=1024), None)
        if chunk:
            print(f"   Data received: {len(chunk)} bytes")
            print(f"   ✓ Main app is proxying!")
        else:
            print(f"   ✗ No data received")
    else:
        print(f"   ✗ Failed")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test direct DroidCam
droidcam_url = "http://192.168.29.220:4747/video"
print(f"\n3. Direct DroidCam URL:")
print(f"   {droidcam_url}")
try:
    response = requests.get(droidcam_url, stream=True, timeout=5)
    print(f"   Status: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
    if response.status_code == 200:
        chunk = next(response.iter_content(chunk_size=1024), None)
        if chunk:
            print(f"   Data received: {len(chunk)} bytes")
            if b'\xff\xd8' in chunk:
                print(f"   ✓✓ MJPEG stream working!")
            else:
                print(f"   ✗ Not MJPEG data")
        else:
            print(f"   ✗ No data received")
    else:
        print(f"   ✗ Failed")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 60)
print("\nRECOMMENDATION:")
print("If direct DroidCam works but camera service doesn't,")
print("check the camera service terminal for error messages.")
