import requests

# Test if authentication works for camera feed
session = requests.Session()

# First, try without login
print("1. Testing without login...")
url = 'http://localhost:8000/cameras/camera-feed/9/'
response = session.get(url, stream=True, timeout=5)
print(f"   Status: {response.status_code}")
print(f"   Content-Type: {response.headers.get('Content-Type')}")
if response.status_code != 200:
    print(f"   Response: {response.text[:200]}")

# Now login
print("\n2. Logging in as Admin...")
login_url = 'http://localhost:8000/login/'
# First get the login page to get CSRF token
login_page = session.get(login_url)
csrf_token = None
for line in login_page.text.split('\n'):
    if 'csrfmiddlewaretoken' in line:
        # Extract token from input field
        import re
        match = re.search(r'value="([^"]+)"', line)
        if match:
            csrf_token = match.group(1)
            break

if csrf_token:
    print(f"   CSRF Token: {csrf_token[:20]}...")
    login_data = {
        'username': 'Admin',
        'password': 'admin123',
        'csrfmiddlewaretoken': csrf_token
    }
    response = session.post(login_url, data=login_data, headers={'Referer': login_url})
    print(f"   Login Status: {response.status_code}")
    print(f"   Cookies: {list(session.cookies.keys())}")
else:
    print("   Could not find CSRF token")

# Try again with login
print("\n3. Testing with login...")
response = session.get(url, stream=True, timeout=5)
print(f"   Status: {response.status_code}")
print(f"   Content-Type: {response.headers.get('Content-Type')}")

if response.status_code == 200:
    print("   ✓ Feed is accessible!")
    # Read first chunk
    chunk = next(response.iter_content(chunk_size=1024))
    print(f"   First chunk size: {len(chunk)} bytes")
else:
    print(f"   ✗ Error: {response.text[:200]}")
