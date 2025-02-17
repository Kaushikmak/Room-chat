from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('room/<str:pagekey>/', views.room, name="room"),
    path('create-room/', views.createRoom, name="create-room"),
    path('create-topic/', views.createTopic, name="create-topic"),
    path('update-room/<str:pagekey>/', views.updateRoom, name="update-room"),
    path('delete/<str:pagekey>/', views.deleteRoom, name="delete-room"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name='register-user'),
    path('deletemessage/<str:pagekey>/', views.deleteMessage, name="delete-message"),
    path('profilepage/<str:pagekey>/', views.profilePage, name='user-profile'),
]