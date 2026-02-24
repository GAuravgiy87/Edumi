import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_project.settings')
django.setup()

from mobile_cameras.models import MobileCamera

cam = MobileCamera.objects.get(id=7)
print(f"Before: {cam.get_stream_url()}")
cam.stream_path = '/video'
cam.save()
print(f"After: {cam.get_stream_url()}")
print("✓ Fixed!")
