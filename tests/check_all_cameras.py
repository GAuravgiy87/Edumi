import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_project.settings')
django.setup()

from mobile_cameras.models import MobileCamera

print("\nAll Mobile Cameras:")
for cam in MobileCamera.objects.all():
    print(f"ID {cam.id}: {cam.name} - {cam.get_stream_url()} - Active: {cam.is_active}")
