import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_project.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile

# Update teacher profile
try:
    teacher = User.objects.get(username='teacher')
    teacher.first_name = 'John'
    teacher.last_name = 'Smith'
    teacher.email = 'john.smith@edumi.edu'
    teacher.save()
    
    profile = teacher.userprofile
    profile.bio = 'Experienced mathematics teacher with 10+ years of teaching experience. Passionate about making complex concepts simple and engaging for students.'
    profile.phone = '+1 (555) 123-4567'
    profile.date_of_birth = date(1985, 5, 15)
    profile.address = '123 Education Street, Learning City, LC 12345'
    profile.employee_id = 'TCH001'
    profile.department = 'Mathematics'
    profile.specialization = 'Calculus, Algebra, Geometry'
    profile.join_date = date(2015, 9, 1)
    profile.linkedin = 'https://linkedin.com/in/johnsmith'
    profile.website = 'https://johnsmith-math.com'
    profile.save()
    
    print("✓ Teacher profile updated")
except Exception as e:
    print(f"❌ Error updating teacher: {e}")

# Update student profile
try:
    student = User.objects.get(username='student')
    student.first_name = 'Emma'
    student.last_name = 'Johnson'
    student.email = 'emma.johnson@student.edumi.edu'
    student.save()
    
    profile = student.userprofile
    profile.bio = 'Enthusiastic learner with a passion for mathematics and science. Active participant in school clubs and competitions.'
    profile.phone = '+1 (555) 987-6543'
    profile.date_of_birth = date(2008, 8, 20)
    profile.address = '456 Student Avenue, Learning City, LC 12345'
    profile.student_id = 'STU2024001'
    profile.grade = '10th Grade'
    profile.enrollment_date = date(2020, 9, 1)
    profile.twitter = 'https://twitter.com/emmajohnson'
    profile.save()
    
    print("✓ Student profile updated")
except Exception as e:
    print(f"❌ Error updating student: {e}")

print("\n=== Profile Update Complete ===")
print("\nYou can now view profiles at:")
print("Teacher: http://127.0.0.1:8000/profile/teacher/")
print("Student: http://127.0.0.1:8000/profile/student/")
print("\nAdmin Panel: http://127.0.0.1:8000/admin-panel/")
