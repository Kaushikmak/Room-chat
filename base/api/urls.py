from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    
    # User Operations
    path('users/register/', views.registerUser, name='register-user'),
    path('users/profile/', views.manageUser, name='user-profile'),

    # Room Operations
    path('rooms/', views.roomList, name='room-list'),
    path('rooms/<str:pk>/', views.roomDetail, name='room-detail'),
    
    # Message Operations
    path('rooms/<str:pk>/messages/', views.roomMessages, name='room-messages'),

    # --- MISSING ENDPOINTS ADDED HERE ---
    path('topics/', views.getTopics, name='get-topics'),
    path('activity/', views.getActivity, name='get-activity'),
    path('users/login/', views.loginUser, name='login-user'), # New Login
    path('rooms/<str:pk>/join/', views.toggleJoin, name='toggle-join'), # New Join/Leave
]