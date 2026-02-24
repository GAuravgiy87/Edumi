"""Quick script to pause/resume mobile cameras from command line"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_project.settings')
django.setup()

from mobile_cameras.models import MobileCamera

def list_cameras():
    """List all cameras with their status"""
    cameras = MobileCamera.objects.all()
    print("\n=== Mobile Cameras ===")
    for camera in cameras:
        status = "✓ Active" if camera.is_active else "⏸ Paused"
        print(f"{camera.id}. {camera.name} - {status}")
        print(f"   {camera.ip_address}:{camera.port}{camera.stream_path}")
    print()

def pause_camera(camera_id):
    """Pause a camera"""
    try:
        camera = MobileCamera.objects.get(id=camera_id)
        camera.is_active = False
        camera.save()
        print(f"✓ Paused camera {camera.id}: {camera.name}")
    except MobileCamera.DoesNotExist:
        print(f"✗ Camera {camera_id} not found")

def resume_camera(camera_id):
    """Resume a camera"""
    try:
        camera = MobileCamera.objects.get(id=camera_id)
        camera.is_active = True
        camera.save()
        print(f"✓ Resumed camera {camera.id}: {camera.name}")
    except MobileCamera.DoesNotExist:
        print(f"✗ Camera {camera_id} not found")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python pause_camera.py list")
        print("  python pause_camera.py pause <camera_id>")
        print("  python pause_camera.py resume <camera_id>")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'list':
        list_cameras()
    elif command == 'pause':
        if len(sys.argv) < 3:
            print("Error: Please provide camera ID")
            sys.exit(1)
        pause_camera(int(sys.argv[2]))
        list_cameras()
    elif command == 'resume':
        if len(sys.argv) < 3:
            print("Error: Please provide camera ID")
            sys.exit(1)
        resume_camera(int(sys.argv[2]))
        list_cameras()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
