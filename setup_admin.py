import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_project.settings')
django.setup()

from django.contrib.auth.models import User

# Create Admin user
try:
    admin_user = User.objects.create_user(username='Admin', password='Admin')
    print("✓ Admin user created (Username: Admin, Password: Admin)")
except:
    print("✓ Admin user already exists")

print("\n=== Setup Complete ===")
print("Login with:")
print("Username: Admin")
print("Password: Admin")

