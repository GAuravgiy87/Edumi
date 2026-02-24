import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_project.settings')
django.setup()

from django.contrib.auth.models import User
from meetings.models import Meeting

# Get teacher user
try:
    teacher = User.objects.get(username='teacher')
    
    # Create a test meeting scheduled for 1 hour from now
    scheduled_time = datetime.now() + timedelta(hours=1)
    
    meeting = Meeting.objects.create(
        title='Mathematics Class - Introduction to Calculus',
        description='We will cover basic concepts of derivatives and limits. Please come prepared with questions!',
        teacher=teacher,
        meeting_code='MATH101ABC',
        scheduled_time=scheduled_time,
        duration_minutes=60,
        status='scheduled',
        allow_screen_share=True,
        allow_chat=True,
    )
    
    print("✓ Test meeting created successfully!")
    print(f"\nMeeting Details:")
    print(f"  Title: {meeting.title}")
    print(f"  Code: {meeting.meeting_code}")
    print(f"  Scheduled: {meeting.scheduled_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"  Duration: {meeting.duration_minutes} minutes")
    print(f"\nTeacher can start the meeting from: http://127.0.0.1:8000/meetings/teacher/")
    print(f"Students can join from: http://127.0.0.1:8000/meetings/student/")
    
except User.DoesNotExist:
    print("❌ Teacher user not found. Please run setup_test_users.py first.")
except Exception as e:
    print(f"❌ Error: {e}")
