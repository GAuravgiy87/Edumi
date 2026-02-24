from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm
from .models import UserProfile
from meetings.models import Meeting
from cameras.models import Camera

def login_view(request):
    if request.user.is_authenticated:
        # Check if admin user
        if request.user.username == 'Admin' or request.user.is_superuser:
            return redirect('admin_panel')
        # Check user type
        if hasattr(request.user, 'userprofile'):
            if request.user.userprofile.user_type == 'teacher':
                return redirect('teacher_dashboard')
            elif request.user.userprofile.user_type == 'student':
                return redirect('student_dashboard')
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect based on user type
            if username == 'Admin' or user.is_superuser:
                return redirect('admin_panel')
            if hasattr(user, 'userprofile'):
                if user.userprofile.user_type == 'teacher':
                    return redirect('teacher_dashboard')
                elif user.userprofile.user_type == 'student':
                    return redirect('student_dashboard')
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid username or password'})
    
    return render(request, 'accounts/login.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user_type = request.POST.get('user_type')
        
        if password1 == password2:
            from django.contrib.auth.models import User
            try:
                user = User.objects.create_user(username=username, password=password1)
                UserProfile.objects.create(user=user, user_type=user_type)
                login(request, user)
                if user_type == 'teacher':
                    return redirect('teacher_dashboard')
                elif user_type == 'student':
                    return redirect('student_dashboard')
                return redirect('home')
            except:
                return render(request, 'accounts/register.html', {'error': 'Username already exists'})
        else:
            return render(request, 'accounts/register.html', {'error': 'Passwords do not match'})
    
    return render(request, 'accounts/register.html')

def home(request):
    return render(request, 'accounts/home.html')

@login_required
def teacher_dashboard(request):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.user_type != 'teacher':
        return redirect('login')
    
    # Get real meeting statistics
    total_meetings = Meeting.objects.filter(teacher=request.user).count()
    live_meetings = Meeting.objects.filter(teacher=request.user, status='live').count()
    scheduled_meetings = Meeting.objects.filter(teacher=request.user, status='scheduled').count()
    
    context = {
        'total_meetings': total_meetings,
        'live_meetings': live_meetings,
        'scheduled_meetings': scheduled_meetings,
    }
    
    return render(request, 'accounts/teacher_dashboard.html', context)

@login_required
def student_dashboard(request):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.user_type != 'student':
        return redirect('login')
    
    profile = request.user.userprofile
    
    # Get real meeting statistics
    available_meetings = Meeting.objects.filter(status__in=['scheduled', 'live']).count()
    attended_meetings = request.user.meetingparticipant_set.count()
    
    # Calculate profile completion
    completion = 0
    if profile.display_name: completion += 10
    if request.user.first_name: completion += 10
    if request.user.last_name: completion += 10
    if request.user.email: completion += 10
    if profile.bio: completion += 15
    if profile.phone: completion += 10
    if profile.date_of_birth: completion += 10
    if profile.address: completion += 10
    if profile.profile_picture or profile.avatar_url: completion += 15
    
    context = {
        'available_meetings': available_meetings,
        'attended_meetings': attended_meetings,
        'profile_completion': completion,
        'profile': profile,
    }
    
    return render(request, 'accounts/student_dashboard.html', context)

@login_required
def profile_view(request, username=None):
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        profile_user = request.user
    
    try:
        profile = profile_user.userprofile
    except UserProfile.DoesNotExist:
        profile = None
    
    # Check if viewing own profile
    is_own_profile = request.user == profile_user
    
    # Handle form submission for own profile
    if is_own_profile and request.method == 'POST' and profile:
        # Update User model (allow empty values)
        request.user.first_name = request.POST.get('first_name', '').strip()
        request.user.last_name = request.POST.get('last_name', '').strip()
        request.user.email = request.POST.get('email', '').strip()
        request.user.save()
        
        # Update UserProfile (allow empty values)
        profile.display_name = request.POST.get('display_name', '').strip()
        profile.bio = request.POST.get('bio', '').strip()
        profile.phone = request.POST.get('phone', '').strip()
        profile.address = request.POST.get('address', '').strip()
        
        # Handle profile picture - check if avatar was selected or file uploaded
        avatar_choice = request.POST.get('avatar_choice', '').strip()
        if request.FILES.get('profile_picture'):
            # File uploaded - save it and clear avatar URL
            profile.profile_picture = request.FILES['profile_picture']
            profile.avatar_url = None
        elif avatar_choice:
            # Avatar selected - save URL and clear uploaded picture
            profile.avatar_url = avatar_choice
            profile.profile_picture = None
        
        # Date of birth (optional)
        dob = request.POST.get('date_of_birth', '').strip()
        if dob:
            profile.date_of_birth = dob
        else:
            profile.date_of_birth = None
        
        # Social links (optional)
        profile.linkedin = request.POST.get('linkedin', '').strip()
        profile.twitter = request.POST.get('twitter', '').strip()
        profile.website = request.POST.get('website', '').strip()
        
        # Type-specific fields (optional)
        if profile.user_type == 'student':
            profile.student_id = request.POST.get('student_id', '').strip()
            profile.grade = request.POST.get('grade', '').strip()
            enrollment = request.POST.get('enrollment_date', '').strip()
            if enrollment:
                profile.enrollment_date = enrollment
            else:
                profile.enrollment_date = None
        elif profile.user_type == 'teacher':
            profile.employee_id = request.POST.get('employee_id', '').strip()
            profile.department = request.POST.get('department', '').strip()
            profile.specialization = request.POST.get('specialization', '').strip()
            join = request.POST.get('join_date', '').strip()
            if join:
                profile.join_date = join
            else:
                profile.join_date = None
        
        profile.save()
        
        # Add success message
        messages.success(request, 'Profile updated successfully!')
        
        # Redirect to prevent form resubmission
        return redirect('profile_view', username=request.user.username)
    
    # Calculate profile completion
    completion = 0
    if is_own_profile and profile:
        if profile.display_name: completion += 10
        if profile_user.first_name: completion += 10
        if profile_user.last_name: completion += 10
        if profile_user.email: completion += 10
        if profile.bio: completion += 15
        if profile.phone: completion += 10
        if profile.date_of_birth: completion += 10
        if profile.address: completion += 10
        if profile.profile_picture or profile.avatar_url: completion += 15
    
    # Get user statistics
    stats = {}
    if profile_user.is_superuser or profile_user.username == 'Admin':
        # Admin statistics
        stats['total_users'] = User.objects.count()
        stats['total_meetings'] = Meeting.objects.count()
        stats['live_meetings'] = Meeting.objects.filter(status='live').count()
        stats['total_cameras'] = Camera.objects.count()
    elif profile and profile.user_type == 'teacher':
        stats['total_meetings'] = Meeting.objects.filter(teacher=profile_user).count()
        stats['live_meetings'] = Meeting.objects.filter(teacher=profile_user, status='live').count()
        stats['completed_meetings'] = Meeting.objects.filter(teacher=profile_user, status='ended').count()
    elif profile and profile.user_type == 'student':
        stats['enrolled_courses'] = 6  # Placeholder
        stats['completed_assignments'] = 15  # Placeholder
        stats['meetings_attended'] = profile_user.meetingparticipant_set.count()
    
    context = {
        'profile_user': profile_user,
        'profile': profile,
        'is_own_profile': is_own_profile,
        'stats': stats,
        'completion': completion,
    }
    
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user, user_type='student')
    
    if request.method == 'POST':
        # Update User model
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        # Update UserProfile
        profile.display_name = request.POST.get('display_name', '')
        profile.bio = request.POST.get('bio', '')
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')
        
        # Handle profile picture upload
        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES['profile_picture']
        
        # Date of birth
        dob = request.POST.get('date_of_birth')
        if dob:
            profile.date_of_birth = dob
        
        # Social links
        profile.linkedin = request.POST.get('linkedin', '')
        profile.twitter = request.POST.get('twitter', '')
        profile.website = request.POST.get('website', '')
        
        # Type-specific fields
        if profile.user_type == 'student':
            profile.student_id = request.POST.get('student_id', '')
            profile.grade = request.POST.get('grade', '')
            enrollment = request.POST.get('enrollment_date')
            if enrollment:
                profile.enrollment_date = enrollment
        elif profile.user_type == 'teacher':
            profile.employee_id = request.POST.get('employee_id', '')
            profile.department = request.POST.get('department', '')
            profile.specialization = request.POST.get('specialization', '')
            join = request.POST.get('join_date')
            if join:
                profile.join_date = join
        
        profile.save()
        
        return redirect('profile_view', username=request.user.username)
    
    return render(request, 'accounts/edit_profile.html', {'profile': profile})

@login_required
def admin_panel(request):
    # Check if user is admin
    if request.user.username != 'Admin' and not request.user.is_superuser:
        return redirect('login')
    
    # Get all statistics
    total_users = User.objects.count()
    total_students = UserProfile.objects.filter(user_type='student').count()
    total_teachers = UserProfile.objects.filter(user_type='teacher').count()
    total_meetings = Meeting.objects.count()
    live_meetings = Meeting.objects.filter(status='live').count()
    total_cameras = Camera.objects.count()
    
    # Get recent users
    recent_users = User.objects.order_by('-date_joined')[:10]
    
    # Get all meetings
    all_meetings = Meeting.objects.all()[:20]
    
    # Get all cameras
    all_cameras = Camera.objects.all()
    
    context = {
        'total_users': total_users,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_meetings': total_meetings,
        'live_meetings': live_meetings,
        'total_cameras': total_cameras,
        'recent_users': recent_users,
        'all_meetings': all_meetings,
        'all_cameras': all_cameras,
    }
    
    return render(request, 'accounts/admin_panel.html', context)

@login_required
def user_management(request):
    # Check if user is admin
    if request.user.username != 'Admin' and not request.user.is_superuser:
        return redirect('login')
    
    users = User.objects.all().order_by('-date_joined')
    
    return render(request, 'accounts/user_management.html', {'users': users})

@login_required
def delete_user(request, user_id):
    # Check if user is admin
    if request.user.username != 'Admin' and not request.user.is_superuser:
        return redirect('login')
    
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        if user.username != 'Admin':  # Prevent deleting admin
            user.delete()
    
    return redirect('user_management')
