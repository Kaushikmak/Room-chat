from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

# Imports
from base.models import Room, Topic, Message, Friendship
from django.contrib.auth.models import User
from .serializers import RoomSerializer, MessageSerializer, UserSerializer, TopicSerializer, ActivitySerializer, FriendSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def getRoutes(request):
    routes = [
        'POST /api/users/register/',
        'POST /api/auth/login/',
        'GET /api/rooms/',
        'POST /api/rooms/',
        'GET /api/rooms/<id>/',
        'POST /api/chat/start/',
        'GET /api/users/friends/',
        'POST /api/users/friends/',
    ]
    return Response(routes)

# -----------------------------------------------------------------------------
# AUTH & USER
# -----------------------------------------------------------------------------

@api_view(['POST'])
@permission_classes([AllowAny])
def loginUser(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id, 'username': user.username})
    else:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def registerUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def manageUser(request):
    user = request.user
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# -----------------------------------------------------------------------------
# FRIENDS & DIRECT MESSAGES (NEW)
# -----------------------------------------------------------------------------

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def manageFriends(request, username=None):
    user = request.user

    # GET: List my friends
    if request.method == 'GET':
        friends = Friendship.objects.filter(user=user)
        serializer = FriendSerializer(friends, many=True)
        return Response(serializer.data)

    # POST: Add a friend
    if request.method == 'POST':
        target_username = request.data.get('username')
        if not target_username:
            return Response({'detail': 'Username required'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            target_user = User.objects.get(username=target_username)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if target_user == user:
            return Response({'detail': 'You cannot add yourself'}, status=status.HTTP_400_BAD_REQUEST)

        friendship, created = Friendship.objects.get_or_create(user=user, friend=target_user)
        if created:
            return Response({'status': 'Friend added', 'username': target_user.username})
        return Response({'status': 'Already friends'}, status=status.HTTP_200_OK)

    # DELETE: Remove a friend
    if request.method == 'DELETE':
        try:
            target_user = User.objects.get(username=username)
            Friendship.objects.filter(user=user, friend=target_user).delete()
            return Response({'status': 'Friend removed'})
        except User.DoesNotExist:
             return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def startDirectChat(request):
    """
    Start a DM. Returns existing room if found, or creates new one.
    """
    user = request.user
    target_username = request.data.get('username')
    
    try:
        target_user = User.objects.get(username=target_username)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Find existing private room between these two
    rooms = Room.objects.filter(is_direct_message=True).filter(participants=user).filter(participants=target_user)
    
    if rooms.exists():
        serializer = RoomSerializer(rooms.first())
        return Response(serializer.data)

    # Create new private room
    room = Room.objects.create(
        host=user,
        name=f"DM: {user.username} & {target_user.username}",
        is_direct_message=True,
        topic=None
    )
    room.participants.add(user, target_user)
    
    serializer = RoomSerializer(room)
    return Response(serializer.data)


# -----------------------------------------------------------------------------
# ROOMS
# -----------------------------------------------------------------------------

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def roomList(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        # Only show PUBLIC rooms (not DMs) in the main list
        rooms = Room.objects.filter(is_direct_message=False).filter(
            Q(topic__name__contains=query) |
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

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

    if request.method == 'GET':
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    if room.host != request.user:
        return Response({'detail': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggleJoin(request, pk):
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
            room.participants.add(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------------------------------------------------------
# UTILS
# -----------------------------------------------------------------------------

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def getTopics(request):
    if request.method == 'GET':
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = TopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def getActivity(request):
    # CHANGE: Filter out DMs (is_direct_message=False)
    activities = Message.objects.filter(room__is_direct_message=False).order_by('-created')[:10]
    serializer = ActivitySerializer(activities, many=True)
    return Response(serializer.data)



def soundex(query):
    """
    Basic Soundex algorithm to convert a string into a phonetic code.
    Example: 'John' -> 'J500', 'Jon' -> 'J500'
    """
    query = query.upper()
    if not query: return ""
    
    # 1. Retain first letter
    code = query[0]
    
    # 2. Mapping
    mapping = {
        "BFPV": "1", "CGJKQSXZ": "2", "DT": "3",
        "L": "4", "MN": "5", "R": "6"
    }
    
    # 3. Encode
    prev_digit = mapping.get(query[0], "") if query[0] in "BFPVCGJKQSXZDTLMNR" else ""
    
    for char in query[1:]:
        digit = ""
        for key, val in mapping.items():
            if char in key:
                digit = val
                break
        
        if digit and digit != prev_digit:
            code += digit
            prev_digit = digit
            
    # 4. Pad or Truncate to 4 characters
    code = (code + "0000")[:4]
    return code

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def searchUsers(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return Response([])

    user = request.user
    
    # 1. Get all users except self
    all_users = User.objects.exclude(id=user.id)

    # 2. Get IDs of existing friends to exclude them (optional, but good UX)
    existing_friend_ids = Friendship.objects.filter(user=user).values_list('friend_id', flat=True)
    candidates = all_users.exclude(id__in=existing_friend_ids)

    # 3. Filter: Exact/Partial Match OR Phonetic Match
    results = []
    query_soundex = soundex(query)

    for candidate in candidates:
        # Exact/Partial match (Standard search)
        if query.lower() in candidate.username.lower():
            results.append(candidate)
            continue
        
        # Phonetic match (Fuzzy search)
        # We allow it if the soundex codes match
        if soundex(candidate.username) == query_soundex:
            results.append(candidate)

    # 4. Serialize
    # We use a custom inline serialization for speed
    data = [{'username': u.username, 'id': u.id} for u in results[:10]] # Limit to 10
    return Response(data)