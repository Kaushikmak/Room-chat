from django.urls import path, include
from . import views
from base.views_auth import GoogleLogin, GitHubLogin 

urlpatterns = [
    path('', views.getRoutes),
    
    # --- Authentication ---
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('auth/github/', GitHubLogin.as_view(), name='github_login'),
    path('auth/', include('dj_rest_auth.urls')),

    # --- User Operations ---
    path('users/login/', views.loginUser, name='login-user'),
    path('users/register/', views.registerUser, name='register-user'),
    path('users/profile/', views.manageUser, name='user-profile'),

    # --- Friends (NEW) ---
    path('users/friends/', views.manageFriends, name='list-add-friends'),
    path('users/friends/<str:username>/', views.manageFriends, name='remove-friend'),

    # --- Direct Messaging (NEW) ---
    path('chat/start/', views.startDirectChat, name='start-dm'),

    # --- Room Endpoints ---
    path('rooms/', views.roomList, name='room-list'),
    path('rooms/<str:pk>/', views.roomDetail, name='room-detail'),
    path('rooms/<str:pk>/messages/', views.roomMessages, name='room-messages'),
    path('rooms/<str:pk>/join/', views.toggleJoin, name='toggle-join'),
    
    # --- Utility ---
    path('topics/', views.getTopics, name='get-topics'),
    path('activity/', views.getActivity, name='get-activity'),
]