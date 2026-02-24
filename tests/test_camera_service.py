import requests
import time

# Test if camera service is running
try:
    response = requests.get('http://localhost:8001/api/cameras/', timeout=5)
    print(f"Camera service status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Camera service error: {e}")

# Test camera feed endpoint
print("\nTesting camera feed endpoint...")
try:
    response = requests.get('http://localhost:8001/api/cameras/10/feed/', stream=True, timeout=10)
    print(f"Feed status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    
    # Try to read first chunk
    chunk_count = 0
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            chunk_count += 1
            print(f"Received chunk {chunk_count}, size: {len(chunk)} bytes")
            if chunk_count >= 3:
                break
    print(f"✓ Camera feed is streaming!")
except Exception as e:
    print(f"✗ Feed error: {e}")
