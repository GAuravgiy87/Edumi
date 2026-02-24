"""
Test script for camera permission system
Run with: python test_camera_permissions.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_project.settings')
django.setup()

from django.contrib.auth.models import User
from cameras.models import Camera, CameraPermission
from accounts.models import UserProfile

def test_camera_permissions():
    print("=" * 60)
    print("Testing Camera Permission System")
    print("=" * 60)
    
    # Get or create admin
    admin, _ = User.objects.get_or_create(
        username='Admin',
        defaults={'is_superuser': True, 'is_staff': True}
    )
    print(f"✓ Admin user: {admin.username}")
    
    # Get or create teacher
    teacher, created = User.objects.get_or_create(
        username='teacher1',
        defaults={'first_name': 'John', 'last_name': 'Smith'}
    )
    if created:
        teacher.set_password('teacher123')
        teacher.save()
        UserProfile.objects.create(
            user=teacher,
            user_type='teacher',
            employee_id='T001',
            department='Mathematics'
        )
    print(f"✓ Teacher user: {teacher.username}")
    
    # Get or create student
    student, created = User.objects.get_or_create(
        username='student1',
        defaults={'first_name': 'Jane', 'last_name': 'Doe'}
    )
    if created:
        student.set_password('student123')
        student.save()
        UserProfile.objects.create(
            user=student,
            user_type='student',
            student_id='S001',
            grade='10th Grade'
        )
    print(f"✓ Student user: {student.username}")
    
    # Create test camera
    camera, created = Camera.objects.get_or_create(
        name='Test Camera 1',
        defaults={
            'rtsp_url': 'rtsp://192.168.1.100:554/stream',
            'ip_address': '192.168.1.100',
            'port': 554,
            'stream_path': '/stream',
            'is_active': True
        }
    )
    print(f"✓ Test camera: {camera.name}")
    
    print("\n" + "=" * 60)
    print("Testing Permissions")
    print("=" * 60)
    
    # Test 1: Admin has access
    print(f"\n1. Admin access to camera: {camera.has_permission(admin)}")
    assert camera.has_permission(admin) == True, "Admin should have access"
    print("   ✓ PASS: Admin has access")
    
    # Test 2: Teacher without permission
    print(f"\n2. Teacher access (no permission): {camera.has_permission(teacher)}")
    assert camera.has_permission(teacher) == False, "Teacher should not have access"
    print("   ✓ PASS: Teacher denied without permission")
    
    # Test 3: Grant permission to teacher
    permission, created = CameraPermission.objects.get_or_create(
        camera=camera,
        teacher=teacher,
        defaults={'granted_by': admin}
    )
    print(f"\n3. Permission granted to teacher: {created or 'Already exists'}")
    print(f"   Teacher access (with permission): {camera.has_permission(teacher)}")
    assert camera.has_permission(teacher) == True, "Teacher should have access after grant"
    print("   ✓ PASS: Teacher has access after permission granted")
    
    # Test 4: List authorized teachers
    authorized = camera.get_authorized_teachers()
    print(f"\n4. Authorized teachers: {[t.username for t in authorized]}")
    assert teacher in authorized, "Teacher should be in authorized list"
    print("   ✓ PASS: Teacher in authorized list")
    
    # Test 5: Revoke permission
    CameraPermission.objects.filter(camera=camera, teacher=teacher).delete()
    print(f"\n5. Permission revoked from teacher")
    print(f"   Teacher access (after revoke): {camera.has_permission(teacher)}")
    assert camera.has_permission(teacher) == False, "Teacher should not have access after revoke"
    print("   ✓ PASS: Teacher denied after permission revoked")
    
    # Test 6: Multiple permissions
    teacher2, created = User.objects.get_or_create(
        username='teacher2',
        defaults={'first_name': 'Sarah', 'last_name': 'Johnson'}
    )
    if created:
        teacher2.set_password('teacher123')
        teacher2.save()
        UserProfile.objects.create(
            user=teacher2,
            user_type='teacher',
            employee_id='T002',
            department='Science'
        )
    
    CameraPermission.objects.create(camera=camera, teacher=teacher, granted_by=admin)
    CameraPermission.objects.create(camera=camera, teacher=teacher2, granted_by=admin)
    
    authorized = camera.get_authorized_teachers()
    print(f"\n6. Multiple permissions: {[t.username for t in authorized]}")
    assert len(authorized) == 2, "Should have 2 authorized teachers"
    print("   ✓ PASS: Multiple permissions work correctly")
    
    print("\n" + "=" * 60)
    print("All Tests Passed! ✓")
    print("=" * 60)
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Total Cameras: {Camera.objects.count()}")
    print(f"Total Permissions: {CameraPermission.objects.count()}")
    print(f"Teachers with access to '{camera.name}': {authorized.count()}")
    print("\nPermission Details:")
    for perm in CameraPermission.objects.filter(camera=camera):
        print(f"  - {perm.teacher.username} (granted by {perm.granted_by.username} on {perm.granted_at.strftime('%Y-%m-%d %H:%M')})")

if __name__ == '__main__':
    try:
        test_camera_permissions()
    except Exception as e:
        print(f"\n❌ Test Failed: {e}")
        import traceback
        traceback.print_exc()
