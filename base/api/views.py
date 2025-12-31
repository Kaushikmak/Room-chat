from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from base.models import Room, Topic, Message
from .serializers import RoomSerializer, MessageSerializer, UserSerializer, TopicSerializer, ActivitySerializer
from base.models import Topic

@api_view(['GET'])
@permission_classes([AllowAny])
def getRoutes(request):
    routes = [
        'POST /api/users/register/',
        'GET /api/users/profile/',
        'PUT /api/users/profile/',
        'DELETE /api/users/profile/',
        'GET /api/rooms/',
        'POST /api/rooms/',
        'GET /api/rooms/<id>/',
        'GET /api/rooms/<id>/messages/',
        'POST /api/rooms/<id>/messages/',
    ]
    return Response(routes)

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

# ... existing imports ...

# 1. LOGIN VIEW
@api_view(['POST'])
@permission_classes([AllowAny])
def loginUser(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        })
    else:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# 2. JOIN/LEAVE VIEW
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggleJoin(request, pk):
    """
    Toggles the user's participation in a room.
    POST /api/rooms/<id>/join/
    """
    try:
        room = Room.objects.get(id=pk)
    except Room.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user in room.participants.all():
        room.participants.remove(request.user)
        return Response({'status': 'left', 'room': room.name})
    else:
        room.participants.add(request.user)
        return Response({'status': 'joined', 'room': room.name})

# 3. UPDATE roomMessages TO ADD PARTICIPANT AUTOMATICALLY
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def roomMessages(request, pk):
    try:
        room = Room.objects.get(id=pk)
    except Room.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        messages = room.message_set.all().order_by('created')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, room=room)
            
            # --- ADD THIS LINE ---
            room.participants.add(request.user) 
            # ---------------------
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------------------------------------------------------
# USER MANAGEMENT ENDPOINTS
# -----------------------------------------------------------------------------

@api_view(['POST'])
@permission_classes([AllowAny])
def registerUser(request):
    """
    Create a new user. Publicly accessible.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def manageUser(request):
    """
    Manage the currently logged-in user's account.
    Requires Authentication (Token or Basic Auth).
    """
    user = request.user
    
    # View Profile
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    # Update Profile (partial=True allows updating just one field like username)
    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete Account
    if request.method == 'DELETE':
        user.delete()
        return Response({'detail': 'Account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# -----------------------------------------------------------------------------
# ROOM ENDPOINTS
# -----------------------------------------------------------------------------

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def roomList(request):
    # GET: List all rooms (Searchable via ?q=)
    if request.method == 'GET':
        query = request.GET.get('q', '')
        rooms = Room.objects.filter(
            Q(topic__name__contains=query) |
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    # POST: Create a new room
    if request.method == 'POST':
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(host=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def roomDetail(request, pk):
    try:
        room = Room.objects.get(id=pk)
    except Room.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # GET: Retrieve single room
    if request.method == 'GET':
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    # Check permissions for PUT/DELETE
    if room.host != request.user:
        return Response(
            {'detail': 'You do not have permission to perform this action.'}, 
            status=status.HTTP_403_FORBIDDEN
        )

    # PUT: Update room
    if request.method == 'PUT':
        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE: Delete room
    if request.method == 'DELETE':
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -----------------------------------------------------------------------------
# MESSAGE ENDPOINTS
# -----------------------------------------------------------------------------

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def roomMessages(request, pk):
    try:
        room = Room.objects.get(id=pk)
    except Room.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # GET: List messages in this room
    if request.method == 'GET':
        messages = room.message_set.all().order_by('created')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    # POST: Create message in this room
    if request.method == 'POST':
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            # Automatically attach user and room
            serializer.save(user=request.user, room=room)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



# --- NEW ENDPOINTS ---

@api_view(['GET'])
@permission_classes([AllowAny])
def getTopics(request):
    """
    GET /api/topics/
    Returns a list of all topics (id, name) so the frontend can populate dropdowns.
    """
    topics = Topic.objects.all()
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def getActivity(request):
    """
    GET /api/activity/
    Returns the 5 most recent messages from ANY room (for the Activity Sidebar).
    """
    # Get last 5 messages
    activities = Message.objects.all().order_by('-created')[:5]
    serializer = ActivitySerializer(activities, many=True)
    return Response(serializer.data)