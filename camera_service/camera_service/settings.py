"""Camera Service Settings - Dedicated RTSP streaming service"""
from pathlib import Path
import os
import sys

# Add parent directory to path to access main project's database
BASE_DIR = Path(__file__).resolve().parent.parent
MAIN_PROJECT_DIR = BASE_DIR.parent

sys.path.insert(0, str(MAIN_PROJECT_DIR))

SECRET_KEY = 'camera-service-key-change-in-production'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'corsheaders',
    'cameras',  # Need Camera model
    'camera_api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

# CORS settings - allow main app to access camera service
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'camera_service.urls'

# Use the same database as main project
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': MAIN_PROJECT_DIR / 'db.sqlite3',
    }
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'camera_api': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
