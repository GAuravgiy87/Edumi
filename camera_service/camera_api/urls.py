"""Camera API URLs"""
from django.urls import path
from . import views

urlpatterns = [
    path('cameras/', views.list_cameras, name='list_cameras'),
    path('cameras/<int:camera_id>/feed/', views.camera_feed, name='camera_feed'),
    path('cameras/<int:camera_id>/test/', views.test_camera, name='test_camera'),
]
