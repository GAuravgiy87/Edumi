import socket
import time

def check_port(port, name):
    """Check if a port is in use"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    
    if result == 0:
        print(f"✓ {name} is running on port {port}")
        return True
    else:
        print(f"✗ {name} is NOT running on port {port}")
        return False

print("Checking services...")
print("=" * 60)

# Check main app
main_running = check_port(8000, "Main App")

# Check camera service
camera_running = check_port(8001, "Camera Service")

print("=" * 60)

if main_running and camera_running:
    print("\n✓ Both services are running!")
    print("\nYou can now access:")
    print("  Main App: http://localhost:8000")
    print("  Camera Service: http://localhost:8001")
elif main_running:
    print("\n⚠ Only Main App is running")
    print("\nTo start Camera Service:")
    print("  cd camera_service")
    print("  python manage.py runserver 8001")
elif camera_running:
    print("\n⚠ Only Camera Service is running")
    print("\nTo start Main App:")
    print("  python manage.py runserver 8000")
else:
    print("\n✗ No services are running")
    print("\nTo start both services:")
    print("  Option 1: Run .\\start_services.bat")
    print("  Option 2: Start manually in two terminals:")
    print("    Terminal 1: cd camera_service && python manage.py runserver 8001")
    print("    Terminal 2: python manage.py runserver 8000")
