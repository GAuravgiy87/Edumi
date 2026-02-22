import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import MobileCamera, MobileCameraPermission

logger = logging.getLogger('mobile_cameras')


def is_admin(user):
    """Check if user is admin"""
    if user.is_authenticated:
        if user.username == 'Admin' or user.username == 'admin' or user.is_superuser:
            return True
    return False


def can_view_mobile_camera(user, mobile_camera):
    """Check if user can view a specific mobile camera"""
    if is_admin(user):
        return True
    # Teachers can view mobile cameras they have permission for
    if hasattr(user, 'userprofile') and user.userprofile.user_type == 'teacher':
        return mobile_camera.has_permission(user)
    # Students can view all active mobile cameras
    if hasattr(user, 'userprofile') and user.userprofile.user_type == 'student':
        return mobile_camera.is_active
    return False


@login_required
def mobile_camera_dashboard(request):
    """Dashboard for managing mobile cameras"""
    if not is_admin(request.user):
        return redirect('login')
    
    mobile_cameras = MobileCamera.objects.all()
    teachers = User.objects.filter(userprofile__user_type='teacher')
    
    # Get permissions for each mobile camera
    mobile_camera_permissions = {}
    for mobile_camera in mobile_cameras:
        mobile_camera_permissions[mobile_camera.id] = mobile_camera.get_authorized_teachers()
    
    context = {
        'mobile_cameras': mobile_cameras,
        'teachers': teachers,
        'mobile_camera_permissions': mobile_camera_permissions,
    }
    return render(request, 'mobile_cameras/dashboard.html', context)


@login_required
def add_mobile_camera(request):
    """Add a new mobile camera"""
    if not is_admin(request.user):
        return redirect('login')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        camera_type = request.POST.get('camera_type')
        ip_address = request.POST.get('ip_address')
        port = int(request.POST.get('port', 8080))
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        stream_path = request.POST.get('stream_path', '/video')
        
        # Create mobile camera
        MobileCamera.objects.create(
            name=name,
            camera_type=camera_type,
            ip_address=ip_address,
            port=port,
            username=username,
            password=password,
            stream_path=stream_path,
            is_active=True
        )
        return redirect('mobile_cameras:dashboard')
    
    return render(request, 'mobile_cameras/add_camera.html')


@login_required
def delete_mobile_camera(request, mobile_camera_id):
    """Delete a mobile camera"""
    if not is_admin(request.user):
        return redirect('login')
    
    mobile_camera = get_object_or_404(MobileCamera, id=mobile_camera_id)
    mobile_camera.delete()
    logger.info(f"Deleted mobile camera {mobile_camera_id}")
    return redirect('mobile_cameras:dashboard')


def mobile_camera_feed(request, mobile_camera_id):
    """Proxy mobile camera feed from camera service on port 8001"""
    mobile_camera = get_object_or_404(MobileCamera, id=mobile_camera_id)
    
    # Check authentication - but don't redirect, just return 403
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=403)
    
    # Check permission
    if not can_view_mobile_camera(request.user, mobile_camera):
        logger.warning(f"User {request.user.username} denied access to mobile camera {mobile_camera_id}")
        return JsonResponse({'error': 'You do not have permission to view this camera'}, status=403)
    
    import requests
    
    def generate_frames():
        """Proxy frames from camera service on port 8001"""
        camera_service_url = f"http://localhost:8001/api/mobile-cameras/{mobile_camera_id}/feed/"
        logger.info(f"Proxying mobile camera feed from: {camera_service_url}")
        
        try:
            response = requests.get(camera_service_url, stream=True, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"Successfully connected to camera service for mobile camera {mobile_camera_id}")
                
                for chunk in response.iter_content(chunk_size=4096):
                    if chunk:
                        yield chunk
            else:
                logger.error(f"Camera service returned HTTP {response.status_code} for mobile camera {mobile_camera_id}")
                error_msg = f"Camera service error: HTTP {response.status_code}"
                yield error_msg.encode()
                        
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Cannot connect to camera service: {e}")
            error_msg = "Camera service not available. Please ensure it's running on port 8001."
            yield error_msg.encode()
        except requests.exceptions.Timeout as e:
            logger.error(f"Timeout connecting to camera service: {e}")
        except GeneratorExit:
            logger.info(f"Client disconnected from mobile camera {mobile_camera_id}")
        except Exception as e:
            logger.error(f"Unexpected error proxying mobile camera {mobile_camera_id}: {e}")
            import traceback
            logger.error(traceback.format_exc())
    
    response = StreamingHttpResponse(
        generate_frames(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    response['X-Accel-Buffering'] = 'no'
    return response


@login_required
def view_mobile_camera(request, mobile_camera_id):
    """View a specific mobile camera"""
    mobile_camera = get_object_or_404(MobileCamera, id=mobile_camera_id)
    
    # Check permission
    if not can_view_mobile_camera(request.user, mobile_camera):
        return redirect('login')
    
    return render(request, 'mobile_cameras/view_camera.html', {'mobile_camera': mobile_camera})


@login_required
def live_monitor(request):
    """View all mobile cameras in a grid"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Filter mobile cameras based on user permissions
    if is_admin(request.user):
        mobile_cameras = MobileCamera.objects.filter(is_active=True)
    elif hasattr(request.user, 'userprofile'):
        if request.user.userprofile.user_type == 'teacher':
            # Teachers see mobile cameras they have permission for
            mobile_camera_ids = MobileCameraPermission.objects.filter(teacher=request.user).values_list('mobile_camera_id', flat=True)
            mobile_cameras = MobileCamera.objects.filter(id__in=mobile_camera_ids, is_active=True)
        elif request.user.userprofile.user_type == 'student':
            # Students see all active mobile cameras
            mobile_cameras = MobileCamera.objects.filter(is_active=True)
        else:
            mobile_cameras = MobileCamera.objects.none()
    else:
        mobile_cameras = MobileCamera.objects.none()
    
    return render(request, 'mobile_cameras/live_monitor.html', {'mobile_cameras': mobile_cameras})


@login_required
def test_mobile_camera(request, mobile_camera_id):
    """Test mobile camera connection via camera service"""
    if not is_admin(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    mobile_camera = get_object_or_404(MobileCamera, id=mobile_camera_id)
    
    try:
        import requests
        
        # Test via camera service on port 8001
        camera_service_url = f"http://localhost:8001/api/mobile-cameras/{mobile_camera_id}/test/"
        response = requests.get(camera_service_url, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'success':
                mobile_camera.is_active = True
                mobile_camera.save()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Mobile camera is accessible via camera service',
                    'url': result.get('url')
                })
            else:
                mobile_camera.is_active = False
                mobile_camera.save()
                return JsonResponse({
                    'status': 'error',
                    'message': result.get('message', 'Camera test failed')
                })
        else:
            mobile_camera.is_active = False
            mobile_camera.save()
            return JsonResponse({
                'status': 'error',
                'message': f'Camera service returned HTTP {response.status_code}'
            })
            
    except requests.exceptions.ConnectionError:
        return JsonResponse({
            'status': 'error',
            'message': 'Cannot connect to camera service on port 8001. Please ensure it is running.'
        })
    except Exception as e:
        logger.error(f"Error testing mobile camera {mobile_camera_id}: {e}")
        mobile_camera.is_active = False
        mobile_camera.save()
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })


@login_required
def grant_permission(request, mobile_camera_id):
    """Grant mobile camera access to a teacher"""
    if not is_admin(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        mobile_camera = get_object_or_404(MobileCamera, id=mobile_camera_id)
        teacher_id = request.POST.get('teacher_id')
        teacher = get_object_or_404(User, id=teacher_id)
        
        # Verify teacher has teacher profile
        if not hasattr(teacher, 'userprofile') or teacher.userprofile.user_type != 'teacher':
            return JsonResponse({'error': 'User is not a teacher'}, status=400)
        
        # Create or get permission
        permission, created = MobileCameraPermission.objects.get_or_create(
            mobile_camera=mobile_camera,
            teacher=teacher,
            defaults={'granted_by': request.user}
        )
        
        if created:
            return JsonResponse({'success': True, 'message': f'Access granted to {teacher.username}'})
        else:
            return JsonResponse({'success': False, 'message': 'Permission already exists'})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def revoke_permission(request, mobile_camera_id, teacher_id):
    """Revoke mobile camera access from a teacher"""
    if not is_admin(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    mobile_camera = get_object_or_404(MobileCamera, id=mobile_camera_id)
    teacher = get_object_or_404(User, id=teacher_id)
    
    # Delete permission
    deleted_count = MobileCameraPermission.objects.filter(mobile_camera=mobile_camera, teacher=teacher).delete()[0]
    
    if deleted_count > 0:
        return JsonResponse({'success': True, 'message': f'Access revoked from {teacher.username}'})
    else:
        return JsonResponse({'success': False, 'message': 'Permission not found'})


@login_required
def manage_permissions(request, mobile_camera_id):
    """View to manage permissions for a specific mobile camera"""
    if not is_admin(request.user):
        return redirect('login')
    
    mobile_camera = get_object_or_404(MobileCamera, id=mobile_camera_id)
    all_teachers = User.objects.filter(userprofile__user_type='teacher')
    authorized_teachers = mobile_camera.get_authorized_teachers()
    unauthorized_teachers = all_teachers.exclude(id__in=authorized_teachers.values_list('id', flat=True))
    
    context = {
        'mobile_camera': mobile_camera,
        'authorized_teachers': authorized_teachers,
        'unauthorized_teachers': unauthorized_teachers,
    }
    return render(request, 'mobile_cameras/manage_permissions.html', context)



@login_required
def test_feed(request, mobile_camera_id):
    """Simple test page to debug mobile camera feed via camera service"""
    if not is_admin(request.user):
        return redirect('login')
    
    mobile_camera = get_object_or_404(MobileCamera, id=mobile_camera_id)
    
    # Test via camera service
    import requests
    stream_url = mobile_camera.get_stream_url()
    camera_service_url = f"http://localhost:8001/api/mobile-cameras/{mobile_camera_id}/test/"
    
    try:
        response = requests.get(camera_service_url, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            context = {
                'mobile_camera': mobile_camera,
                'stream_url': stream_url,
                'camera_service_url': camera_service_url,
                'status': result.get('status'),
                'message': result.get('message'),
                'success': result.get('status') == 'success',
            }
        else:
            context = {
                'mobile_camera': mobile_camera,
                'stream_url': stream_url,
                'camera_service_url': camera_service_url,
                'error': f'Camera service returned HTTP {response.status_code}',
                'success': False,
            }
    except requests.exceptions.ConnectionError:
        context = {
            'mobile_camera': mobile_camera,
            'stream_url': stream_url,
            'camera_service_url': camera_service_url,
            'error': 'Cannot connect to camera service on port 8001',
            'success': False,
        }
    except Exception as e:
        context = {
            'mobile_camera': mobile_camera,
            'stream_url': stream_url,
            'camera_service_url': camera_service_url,
            'error': str(e),
            'success': False,
        }
    
    return render(request, 'mobile_cameras/test_feed.html', context)
