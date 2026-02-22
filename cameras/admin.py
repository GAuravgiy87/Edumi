from django.contrib import admin
from .models import Camera, CameraPermission

@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip_address', 'port', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'ip_address')

@admin.register(CameraPermission)
class CameraPermissionAdmin(admin.ModelAdmin):
    list_display = ('camera', 'teacher', 'granted_by', 'granted_at')
    list_filter = ('granted_at',)
    search_fields = ('camera__name', 'teacher__username')
    raw_id_fields = ('camera', 'teacher', 'granted_by')
