import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_project.settings')
django.setup()

from cameras.models import Camera

# Update the test camera with working URL
camera = Camera.objects.get(id=1)
camera.rtsp_url = 'rtsp://test:dei@12@12@10.7.16.48:554/live'
camera.stream_path = '/live'
camera.save()

print("✓ Camera URL updated successfully!")
print(f"New URL: {camera.rtsp_url}")
print("\nNow refresh the camera view page to see the live feed!")
