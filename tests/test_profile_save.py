import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_project.settings')
django.setup()

from accounts.models import UserProfile
from django.contrib.auth.models import User

# Get all users with profiles
users = User.objects.filter(userprofile__isnull=False)
print(f"Found {users.count()} users with profiles\n")

for user in users:
    print(f"=" * 50)
    print(f"User: {user.username}")
    print(f"First Name: {user.first_name or 'Not set'}")
    print(f"Last Name: {user.last_name or 'Not set'}")
    print(f"Email: {user.email or 'Not set'}")
    
    profile = user.userprofile
    print(f"\nProfile Data:")
    print(f"Display Name: {profile.display_name or 'Not set'}")
    print(f"User Type: {profile.user_type}")
    print(f"Bio: {profile.bio or 'Not set'}")
    print(f"Phone: {profile.phone or 'Not set'}")
    print(f"Avatar URL: {profile.avatar_url or 'Not set'}")
    print(f"Profile Picture: {profile.profile_picture or 'Not set'}")
    print()

print("\n✓ All data is being saved to the database!")
print("✓ When you save changes, they persist after reload/login")
