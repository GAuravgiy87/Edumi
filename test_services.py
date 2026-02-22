"""Test script to verify both services are running"""
import requests
import time

def test_main_app():
    """Test main app on port 8000"""
    try:
        response = requests.get('http://localhost:8000', timeout=5)
        if response.status_code == 200:
            print("✓ Main App (8000): Running")
            return True
        else:
            print(f"✗ Main App (8000): Unexpected status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Main App (8000): Not responding - {e}")
        return False

def test_camera_service():
    """Test camera service on port 8001"""
    try:
        response = requests.get('http://localhost:8001/api/cameras/', timeout=5)
        if response.status_code == 200:
            print("✓ Camera Service (8001): Running")
            data = response.json()
            print(f"  Found {len(data.get('cameras', []))} active cameras")
            return True
        else:
            print(f"✗ Camera Service (8001): Unexpected status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Camera Service (8001): Not responding - {e}")
        return False

if __name__ == '__main__':
    print("Testing Microservices Architecture...")
    print("-" * 50)
    
    main_ok = test_main_app()
    camera_ok = test_camera_service()
    
    print("-" * 50)
    if main_ok and camera_ok:
        print("\n✓ All services running correctly!")
    else:
        print("\n✗ Some services are not running")
        print("\nMake sure to start services:")
        print("  Windows: start_services.bat")
        print("  Linux/Mac: ./start_services.sh")
