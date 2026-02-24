import requests

print("=" * 60)
print("SERVICE STATUS CHECK")
print("=" * 60)

# Check camera service
try:
    response = requests.get('http://localhost:8001/api/cameras/', timeout=2)
    if response.status_code == 200:
        print("✓ Camera Service (port 8001): RUNNING")
        cameras = response.json().get('cameras', [])
        print(f"  Found {len(cameras)} camera(s)")
        for cam in cameras:
            print(f"    - Camera {cam['id']}: {cam['name']} ({'Active' if cam['is_active'] else 'Inactive'})")
    else:
        print(f"✗ Camera Service (port 8001): ERROR {response.status_code}")
except Exception as e:
    print(f"✗ Camera Service (port 8001): NOT RUNNING - {e}")

print()

# Check main app
try:
    response = requests.get('http://localhost:8000/cameras/admin-dashboard/', timeout=2)
    if response.status_code == 200:
        print("✓ Main App (port 8000): RUNNING")
    else:
        print(f"✗ Main App (port 8000): ERROR {response.status_code}")
except Exception as e:
    print(f"✗ Main App (port 8000): NOT RUNNING - {e}")

print()
print("=" * 60)
print("NEXT STEPS:")
print("=" * 60)
print("1. Open browser: http://localhost:8000")
print("2. Login as admin")
print("3. Go to: Cameras > Admin Dashboard")
print("4. Click 'Live Monitor' to see all camera feeds")
print("5. Or click 'View' on any camera to see individual feed")
print()
print("The RTSP camera feed should now be displaying!")
print("=" * 60)
