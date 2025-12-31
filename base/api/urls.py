from django.urls import path, include
from . import views
# Import the social views from the base folder
from base.views_auth import GoogleLogin, GitHubLogin 

urlpatterns = [
    path('', views.getRoutes),
    
    # --- Social Auth (MOVED HERE) ---
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('auth/github/', GitHubLogin.as_view(), name='github_login'),

    # --- Feature Request: User Updates (Password/Profile) ---
    # This single line adds endpoints for changing password, updating email, etc.
    path('auth/', include('dj_rest_auth.urls')), 

    # User Operations (Your Custom Views)
    path('users/register/', views.registerUser, name='register-user'),
    path('users/profile/', views.manageUser, name='user-profile'),

    # ... keep your existing room endpoints below ...
    path('rooms/', views.roomList, name='room-list'),
    path('rooms/<str:pk>/', views.roomDetail, name='room-detail'),
    path('rooms/<str:pk>/messages/', views.roomMessages, name='room-messages'),
    path('rooms/<str:pk>/join/', views.toggleJoin, name='toggle-join'),
    path('topics/', views.getTopics, name='get-topics'),
    path('activity/', views.getActivity, name='get-activity'),
    path('auth/', include('dj_rest_auth.urls')),
]