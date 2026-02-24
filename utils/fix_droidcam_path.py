"""Fix DroidCam path in database"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_project.settings')
django.setup()

from mobile_cameras.models import MobileCamera

camera = MobileCamera.objects.get(id=6)
print(f"Current path: {camera.stream_path}")
print(f"Current URL: {camera.get_stream_url()}")

camera.stream_path = '/video'
camera.save()

print(f"\nUpdated path: {camera.stream_path}")
print(f"Updated URL: {camera.get_stream_url()}")
print("\n✓ Camera path updated successfully!")
