from django.urls import path
from .views_auth import GoogleLogin, GitHubLogin

# This file is currently unused as we route everything through base/api/urls.py
urlpatterns = [
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('auth/github/', GitHubLogin.as_view(), name='github_login'),
]