from django.shortcuts import render, redirect
from .models import Room, Topic
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
    # query = request.GET.get('q') if request.GET != None else ''
    query = request.GET.get('q', '')  # Default to empty string if q is not in GET

    
    # rooms = Room.objects.all()

    if query == '':
        rooms = Room.objects.all()
    else:
        rooms = Room.objects.filter(topic__name__contains = query)

    topic  = Topic.objects.all()

    context = {'rooms': rooms, 'topic': topic}
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