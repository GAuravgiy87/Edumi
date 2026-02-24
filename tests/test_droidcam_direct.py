"""Test DroidCam connection directly"""
import requests
import sys

if len(sys.argv) < 2:
    print("Usage: python test_droidcam_direct.py <ip_address> [port]")
    print("Example: python test_droidcam_direct.py 10.17.2.141 4747")
    sys.exit(1)

ip = sys.argv[1]
port = sys.argv[2] if len(sys.argv) > 2 else '4747'

print(f"\nTesting DroidCam at {ip}:{port}")
print("="*60)

# Common DroidCam paths
paths = [
    '/mjpegfeed',
    '/video',
    '/videofeed',
    '/cam_1.mjpg',
    '/stream',
    '/',
]

for path in paths:
    url = f"http://{ip}:{port}{path}"
    print(f"\nTrying: {url}")
    
    try:
        response = requests.get(url, timeout=5, stream=True)
        print(f"  Status: {response.status_code}")
        print(f"  Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            if 'image' in content_type or 'video' in content_type or 'multipart' in content_type:
                print(f"  ✓ SUCCESS! This path works!")
                print(f"\nWorking URL: {url}")
                break
            else:
                print(f"  ✗ Wrong content type")
        else:
            print(f"  ✗ Failed")
    except requests.exceptions.Timeout:
        print(f"  ✗ Timeout - camera not responding")
    except requests.exceptions.ConnectionError:
        print(f"  ✗ Connection refused - check IP and port")
    except Exception as e:
        print(f"  ✗ Error: {e}")

print("\n" + "="*60)
print("\nTroubleshooting:")
print("1. Verify DroidCam app is running on your phone")
print("2. Check the IP shown in DroidCam app matches what you entered")
print("3. Ensure phone and computer are on same WiFi network")
print("4. Try accessing the URL in your browser first")
print("5. Check if phone firewall is blocking connections")
