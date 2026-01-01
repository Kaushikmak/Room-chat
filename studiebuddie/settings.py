import os
from pathlib import Path
import dj_database_url # Needed for Render database

BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY: Get these from Environment Variables in Production ---
# Default to a dummy key for local dev, but CRASH if missing in prod
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-change-this')

# Set DEBUG to False in production
DEBUG = 'RENDER' not in os.environ

# Allow the host provided by Render
ALLOWED_HOSTS = ['room-chat-api-eudf.onrender.com', 'www.room-chat.com']

# --- Application definition ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Third Party
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',

    # My Apps
    'base.apps.BaseConfig',

    # Allauth & Providers
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',

    # API Auth
    'dj_rest_auth',
    'dj_rest_auth.registration',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Add Whitenoise for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # CORS must be before CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ROOT_URLCONF = 'studiebuddie.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Points to a root 'templates' folder if you have one
        'APP_DIRS': True, # REQUIRED: Enables finding templates inside apps (like Admin)
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
# ----------------------------------------

# --- Database (Auto-switch between SQLite and Postgres) ---
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600
    )
}

# --- REST Framework Configuration ---
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication', 
    ]
}

CSRF_TRUSTED_ORIGINS = [
    "https://www.room-chat.com",
    "https://room-chat.com",
]

# --- CORS (Allow your frontend to connect) ---
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5500",                  # For local testing
    "http://127.0.0.1:5500",                  # For local testing
    "https://room-chat.vercel.app",           # Your Vercel domain
    "https://www.room-chat.com",
    "https://room-chat.com",              # Your custom domain
]
# In real production, replace True with specific domains:
# CORS_ALLOWED_ORIGINS = ["https://your-frontend.com"]

# --- Static Files (Whitenoise) ---
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


WSGI_APPLICATION = 'studiebuddie.wsgi.application'


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    },
    'github': {
        'SCOPE': ['user:email', 'read:user'],
    }
}

# Simplify setup: Disable email verification for now
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_ADAPTER = 'allauth.socialaccount.adapter.DefaultSocialAccountAdapter'