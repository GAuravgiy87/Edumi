import requests
import time

# Test direct access to camera feed
url = 'http://localhost:8000/cameras/camera-feed/9/'

print("Testing camera feed URL...")
print(f"URL: {url}")

# Create a session to maintain cookies
session = requests.Session()

# First login to get session cookie
login_url = 'http://localhost:8000/login/'
login_data = {
    'username': 'Admin',
    'password': 'admin123'
}

print("\n1. Logging in...")
response = session.post(login_url, data=login_data)
print(f"Login status: {response.status_code}")
print(f"Cookies: {session.cookies.get_dict()}")

# Now try to access camera feed
print("\n2. Accessing camera feed...")
try:
    response = session.get(url, stream=True, timeout=5)
    print(f"Feed status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    
    if response.status_code == 200:
        # Read first few chunks
        print("\n3. Reading stream data...")
        chunk_count = 0
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                chunk_count += 1
                print(f"Received chunk {chunk_count}: {len(chunk)} bytes")
                if chunk_count >= 3:
                    break
        print("✓ Stream is working!")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text[:500])
        
except Exception as e:
    print(f"✗ Error: {e}")
