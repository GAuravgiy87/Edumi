"""Camera Service URL Configuration"""
from django.urls import path, include

urlpatterns = [
    path('api/', include('camera_api.urls')),
]
