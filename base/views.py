from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm

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
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)


def room(request, pagekey):
    # room = None
    # for i in rooms:
    #     if(i['id']==int(pagekey)):
    #         room = i
    room = Room.objects.get(id=pagekey)

    context = {'room': room}
    return render(request, 'base/room.html', context)


def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pagekey):
    room = Room.objects.get(id=pagekey)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room )
        if form.is_valid():
            form.save()
            return redirect('home')


    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pagekey):
    room = Room.objects.get(id=pagekey)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'base/delete.html', context)