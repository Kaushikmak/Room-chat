from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializers


@api_view(['GET'])
def getRoutes(request):
    routes = [
            'GET /api',
            'GET /api/rooms/',
            'GET /api/room/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all();
    serializer = RoomSerializers(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request,roomid):
    room = Room.objects.get(id=roomid)
    serializer = RoomSerializers(room)
    return Response(serializer.data)