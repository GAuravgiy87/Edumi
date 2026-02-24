import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_project.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile

# Create Teacher user
try:
    teacher_user = User.objects.create_user(username='teacher', password='teacher123')
    UserProfile.objects.create(user=teacher_user, user_type='teacher')
    print("✓ Teacher user created (Username: teacher, Password: teacher123)")
except:
    print("✓ Teacher user already exists")

# Create Student user
try:
    student_user = User.objects.create_user(username='student', password='student123')
    UserProfile.objects.create(user=student_user, user_type='student')
    print("✓ Student user created (Username: student, Password: student123)")
except:
    print("✓ Student user already exists")

print("\n=== Test Users Setup Complete ===")
print("\nLogin credentials:")
print("\nTeacher:")
print("  Username: teacher")
print("  Password: teacher123")
print("\nStudent:")
print("  Username: student")
print("  Password: student123")
print("\nAdmin:")
print("  Username: Admin")
print("  Password: Admin")
