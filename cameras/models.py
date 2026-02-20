from django.db import models

class Camera(models.Model):
    name = models.CharField(max_length=100)
    rtsp_url = models.CharField(max_length=500)
    username = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)
    ip_address = models.CharField(max_length=50)
    port = models.IntegerField(default=554)
    stream_path = models.CharField(max_length=200, default='/stream')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def get_full_rtsp_url(self):
        if self.username and self.password:
            return f"rtsp://{self.username}:{self.password}@{self.ip_address}:{self.port}{self.stream_path}"
        return f"rtsp://{self.ip_address}:{self.port}{self.stream_path}"
