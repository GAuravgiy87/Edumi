import requests
import socket

def get_local_ip():
    """Get the local IP address"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

local_ip = get_local_ip()

print("=" * 70)
print("NETWORK ACCESS TEST")
print("=" * 70)
print(f"\nYour Local IP: {local_ip}")
print()

# Test localhost access
print("Testing localhost access...")
try:
    response = requests.get('http://localhost:8000/', timeout=3, allow_redirects=False)
    print(f"✓ Localhost (8000): Accessible (Status: {response.status_code})")
except Exception as e:
    print(f"✗ Localhost (8000): Failed - {e}")

try:
    response = requests.get('http://localhost:8001/api/cameras/', timeout=3)
    print(f"✓ Localhost (8001): Accessible (Status: {response.status_code})")
except Exception as e:
    print(f"✗ Localhost (8001): Failed - {e}")

print()

# Test network IP access
print(f"Testing network IP access ({local_ip})...")
try:
    response = requests.get(f'http://{local_ip}:8000/', timeout=3, allow_redirects=False)
    print(f"✓ Network IP (8000): Accessible (Status: {response.status_code})")
except Exception as e:
    print(f"✗ Network IP (8000): Failed - {e}")

try:
    response = requests.get(f'http://{local_ip}:8001/api/cameras/', timeout=3)
    print(f"✓ Network IP (8001): Accessible (Status: {response.status_code})")
except Exception as e:
    print(f"✗ Network IP (8001): Failed - {e}")

print()
print("=" * 70)
print("SHARE THIS URL WITH OTHERS ON YOUR WIFI:")
print("=" * 70)
print(f"\n    http://{local_ip}:8000\n")
print("=" * 70)
print("\nOthers can access the app by:")
print("1. Connecting to the same WiFi network")
print("2. Opening a browser")
print(f"3. Going to: http://{local_ip}:8000")
print("4. Logging in with their credentials")
print("=" * 70)
