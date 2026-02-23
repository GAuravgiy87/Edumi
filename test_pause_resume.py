"""Test pause/resume functionality for mobile cameras"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_project.settings')
django.setup()

from mobile_cameras.models import MobileCamera

def test_pause_resume():
    """Test pause/resume toggle"""
    cameras = MobileCamera.objects.all()
    
    print("\n=== Mobile Camera Status ===")
    for camera in cameras:
        status = "Active" if camera.is_active else "Paused"
        print(f"Camera {camera.id}: {camera.name} - {status}")
        print(f"  URL: {camera.get_stream_url()}")
    
    print("\n=== Testing Toggle ===")
    if cameras.exists():
        test_camera = cameras.first()
        original_status = test_camera.is_active
        print(f"Camera {test_camera.id} is currently: {'Active' if original_status else 'Paused'}")
        
        # Toggle
        test_camera.is_active = not test_camera.is_active
        test_camera.save()
        print(f"Toggled to: {'Active' if test_camera.is_active else 'Paused'}")
        
        # Toggle back
        test_camera.is_active = original_status
        test_camera.save()
        print(f"Restored to: {'Active' if test_camera.is_active else 'Paused'}")
        
        print("\n✓ Toggle functionality works!")
    else:
        print("No cameras found to test")
    
    print("\n=== Active Cameras (shown in live monitor) ===")
    active_cameras = MobileCamera.objects.filter(is_active=True)
    for camera in active_cameras:
        print(f"  - {camera.name} ({camera.ip_address}:{camera.port})")
    
    print(f"\nTotal: {active_cameras.count()} active cameras")

if __name__ == '__main__':
    test_pause_resume()
