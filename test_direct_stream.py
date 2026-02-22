"""Test streaming directly"""
import requests
import time

print("Testing mobile camera feed...")
print("=" * 60)

# Test camera service directly
print("\n1. Testing Camera Service (port 8001):")
url = "http://localhost:8001/api/mobile-cameras/5/feed/"
print(f"   URL: {url}")

try:
    response = requests.get(url, stream=True, timeout=5)
    print(f"   Status: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('Content-Type')}")
    
    if response.status_code == 200:
        print("   Reading frames...")
        frame_count = 0
        start_time = time.time()
        
        for chunk in response.iter_content(chunk_size=4096):
            if chunk:
                frame_count += 1
                if frame_count <= 5:
                    print(f"   Frame {frame_count}: {len(chunk)} bytes")
                if frame_count >= 10:
                    break
        
        elapsed = time.time() - start_time
        print(f"   ✓ Received {frame_count} frames in {elapsed:.2f} seconds")
        print(f"   ✓✓ Camera service is streaming!")
    else:
        print(f"   ✗ Error: {response.text[:200]}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test main app
print("\n2. Testing Main App (port 8000):")
url = "http://localhost:8000/mobile-cameras/feed/5/"
print(f"   URL: {url}")

try:
    # Need to authenticate
    session = requests.Session()
    
    # Try without auth first
    response = session.get(url, stream=True, timeout=5, allow_redirects=False)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 302:
        print(f"   ✗ Redirected to: {response.headers.get('Location')}")
        print(f"   ✗ Need to login first!")
    elif response.status_code == 200:
        print(f"   Content-Type: {response.headers.get('Content-Type')}")
        print("   Reading frames...")
        frame_count = 0
        
        for chunk in response.iter_content(chunk_size=4096):
            if chunk:
                frame_count += 1
                if frame_count <= 3:
                    print(f"   Frame {frame_count}: {len(chunk)} bytes")
                if frame_count >= 5:
                    break
        
        print(f"   ✓ Received {frame_count} frames")
        print(f"   ✓✓ Main app is proxying!")
    else:
        print(f"   ✗ Error: {response.status_code}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 60)
print("\nCONCLUSION:")
print("If camera service works but main app doesn't,")
print("the issue is authentication or the proxy code.")
