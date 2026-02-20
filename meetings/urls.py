from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_meeting, name='create_meeting'),
    path('teacher/', views.teacher_meetings, name='teacher_meetings'),
    path('student/', views.student_meetings, name='student_meetings'),
    path('join/<str:meeting_code>/', views.join_meeting, name='join_meeting'),
    path('end/<int:meeting_id>/', views.end_meeting, name='end_meeting'),
    path('leave/<int:meeting_id>/', views.leave_meeting, name='leave_meeting'),
    path('participants/<int:meeting_id>/', views.get_participants, name='get_participants'),
    path('delete/<int:meeting_id>/', views.delete_meeting, name='delete_meeting'),
    path('cancel/<int:meeting_id>/', views.cancel_meeting, name='cancel_meeting'),
]
