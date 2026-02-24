"""Check mobile camera in database"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_project.settings')
django.setup()

from mobile_cameras.models import MobileCamera

print("\nMobile Cameras in Database:")
print("="*60)

cameras = MobileCamera.objects.all()
for cam in cameras:
    print(f"\nID: {cam.id}")
    print(f"Name: {cam.name}")
    print(f"Type: {cam.camera_type}")
    print(f"IP: {cam.ip_address}")
    print(f"Port: {cam.port}")
    print(f"Path: {cam.stream_path}")
    print(f"Full URL: {cam.get_stream_url()}")
    print(f"Active: {cam.is_active}")
    print("-"*60)
