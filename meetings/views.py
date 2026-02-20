from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from .models import Meeting, MeetingParticipant
import random
import string

def generate_meeting_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

@login_required
def create_meeting(request):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.user_type != 'teacher':
        return redirect('login')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        scheduled_time = request.POST.get('scheduled_time')
        duration_minutes = int(request.POST.get('duration_minutes', 60))
        allow_screen_share = request.POST.get('allow_screen_share') == 'on'
        allow_chat = request.POST.get('allow_chat') == 'on'
        
        meeting_code = generate_meeting_code()
        
        meeting = Meeting.objects.create(
            title=title,
            description=description,
            teacher=request.user,
            meeting_code=meeting_code,
            scheduled_time=scheduled_time,
            duration_minutes=duration_minutes,
            allow_screen_share=allow_screen_share,
            allow_chat=allow_chat,
        )
        
        return redirect('teacher_meetings')
    
    return render(request, 'meetings/create_meeting.html')

@login_required
def teacher_meetings(request):
    # Allow admin to view all meetings
    if request.user.username == 'Admin' or request.user.is_superuser:
        meetings = Meeting.objects.all()
    elif hasattr(request.user, 'userprofile') and request.user.userprofile.user_type == 'teacher':
        meetings = Meeting.objects.filter(teacher=request.user)
    else:
        return redirect('login')
    
    return render(request, 'meetings/teacher_meetings.html', {
        'meetings': meetings,
        'is_admin': request.user.username == 'Admin' or request.user.is_superuser
    })

@login_required
def student_meetings(request):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.user_type != 'student':
        return redirect('login')
    
    # Get all scheduled and live meetings
    meetings = Meeting.objects.filter(status__in=['scheduled', 'live'])
    return render(request, 'meetings/student_meetings.html', {'meetings': meetings})

@login_required
def join_meeting(request, meeting_code):
    meeting = get_object_or_404(Meeting, meeting_code=meeting_code)
    
    # Create or get participant
    participant, created = MeetingParticipant.objects.get_or_create(
        meeting=meeting,
        user=request.user,
        defaults={'joined_at': timezone.now(), 'is_active': True}
    )
    
    if not created:
        participant.joined_at = timezone.now()
        participant.is_active = True
        participant.save()
    
    # Update meeting status to live if teacher joins
    if meeting.teacher == request.user and meeting.status == 'scheduled':
        meeting.status = 'live'
        meeting.save()
    
    return render(request, 'meetings/meeting_room.html', {
        'meeting': meeting,
        'is_host': meeting.teacher == request.user
    })

@login_required
@require_http_methods(["POST"])
def end_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    
    # Allow teacher or admin to end meeting
    if meeting.teacher != request.user and request.user.username != 'Admin' and not request.user.is_superuser:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'})
    
    meeting.status = 'ended'
    meeting.save()
    
    # Mark all participants as inactive
    MeetingParticipant.objects.filter(meeting=meeting, is_active=True).update(
        is_active=False,
        left_at=timezone.now()
    )
    
    return JsonResponse({'status': 'success'})

@login_required
@require_http_methods(["POST"])
def leave_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    
    try:
        participant = MeetingParticipant.objects.get(meeting=meeting, user=request.user)
        participant.is_active = False
        participant.left_at = timezone.now()
        participant.save()
        return JsonResponse({'status': 'success'})
    except MeetingParticipant.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Not a participant'})

@login_required
def get_participants(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    participants = MeetingParticipant.objects.filter(meeting=meeting, is_active=True)
    
    data = [{
        'id': p.user.id,
        'username': p.user.username,
        'is_host': p.user == meeting.teacher
    } for p in participants]
    
    return JsonResponse({'participants': data})

@login_required
@require_http_methods(["POST"])
def delete_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    
    # Allow teacher or admin to delete meeting
    if meeting.teacher != request.user and request.user.username != 'Admin' and not request.user.is_superuser:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'})
    
    meeting.delete()
    return JsonResponse({'status': 'success'})

@login_required
@require_http_methods(["POST"])
def cancel_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    
    # Allow teacher or admin to cancel meeting
    if meeting.teacher != request.user and request.user.username != 'Admin' and not request.user.is_superuser:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'})
    
    meeting.status = 'cancelled'
    meeting.save()
    return JsonResponse({'status': 'success'})
