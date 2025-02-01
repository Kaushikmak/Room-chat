from django.shortcuts import render
from django.http import HttpResponse
from .models import Room

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