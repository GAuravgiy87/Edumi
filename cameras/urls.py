from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-camera/', views.add_camera, name='add_camera'),
    path('delete-camera/<int:camera_id>/', views.delete_camera, name='delete_camera'),
    path('camera-feed/<int:camera_id>/', views.camera_feed, name='camera_feed'),
    path('view-camera/<int:camera_id>/', views.view_camera, name='view_camera'),
    path('test-camera/<int:camera_id>/', views.test_camera, name='test_camera'),
]
