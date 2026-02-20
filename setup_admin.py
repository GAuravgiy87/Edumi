import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_project.settings')
django.setup()

from django.contrib.auth.models import User
from cameras.models import Camera

# Create Admin user
try:
    admin_user = User.objects.create_user(username='Admin', password='Admin')
    print("✓ Admin user created (Username: Admin, Password: Admin)")
except:
    print("✓ Admin user already exists")

# Add test camera
try:
    camera = Camera.objects.create(
        name='Test Camera',
        rtsp_url='rtsp://test:dei@12@12@10.7.16.48:554/stream',
        username='test',
        password='dei@12@12',
        ip_address='10.7.16.48',
        port=554,
        stream_path='/stream',
        is_active=True
    )
    print("✓ Test camera added successfully")
except Exception as e:
    print(f"Camera already exists or error: {e}")

print("\n=== Setup Complete ===")
print("Login with:")
print("Username: Admin")
print("Password: Admin")
