import requests
import time

print("Testing camera feed from main app...")
try:
    response = requests.get('http://localhost:8000/cameras/camera-feed/10/', stream=True, timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    
    if response.status_code == 200:
        chunk_count = 0
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                chunk_count += 1
                print(f"Received chunk {chunk_count}, size: {len(chunk)} bytes")
                if chunk_count >= 3:
                    break
        print("✓ Feed is working!")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text[:500])
except Exception as e:
    print(f"✗ Error: {e}")
