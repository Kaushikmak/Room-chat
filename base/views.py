from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic, Message
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages


# rooms = [
#     {
#         'id'    :    1,
#         'name'  :   'kaushik'
#     },
#     {
#         'id'    :    2,
#         'name'  :   'yash'
#     },
#     {
#         'id'    :    3,
#         'name'  :   'monkey'
#     },
# ]

def home(request):
    # query = request.GET.get('q') if request.GET != None else ''
    query = request.GET.get('q', '')  # Default to empty string if q is not in GET

    
    # rooms = Room.objects.all()

    if query == '':
        rooms = Room.objects.all()
    else:
        # search by topic name and any value from that key word
        # rooms = Room.objects.filter(topic__name__contains = query)
        rooms = Room.objects.filter(
            Q(topic__name__contains = query) | Q(name__icontains=query) | Q(description__icontains=query)
            )

    topic  = Topic.objects.all()



    room_count = rooms.count()

    context = {'rooms': rooms, 'topic': topic, 'room_count': room_count}
    return render(request, 'base/home.html', context)


def room(request, pagekey):
    # room = None
    # for i in rooms:
    #     if(i['id']==int(pagekey)):
    #         room = i
    room = Room.objects.get(id=pagekey)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pagekey=room.id)


    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def updateRoom(request, pagekey):
    room = Room.objects.get(id=pagekey)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse(f"This is {room.host}'s room you can't edit this")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room )
        if form.is_valid():
            form.save()
            return redirect('home')


    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def deleteRoom(request, pagekey):
    room = Room.objects.get(id=pagekey)

    if request.user != room.host:
        return HttpResponse(f"This is {room.host}'s room you can't delete this")


    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'base/delete.html', context)



def loginPage(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password) 

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Invalid username or password')
            
    return render(request, 'base/login.html')


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    form  = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # for data cleaning don't straight away save this data
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registering user, kindly re-submit details')



    context = {'form': form}
    return render(request, 'base/register.html', context)

@login_required(login_url='/login')
def deleteMessage(request, pagekey):
    msg = Message.objects.get(id=pagekey)
    room = msg.room

    if request.user != msg.user:
        return HttpResponse(f"This is {room.host}'s room you can't delete this")


    if request.method == 'POST':
        msg.delete()
        return redirect('room', pagekey=room.id)
    context = {'obj': msg}
    return render(request, 'base/delete.html', context)
