from rest_framework import serializers
from base.models import Room, Topic, Message
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        # extra_kwargs ensures the password is required when registering 
        # but is NOT included when fetching user data (security best practice).
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        # We override create to use 'create_user' which hashes the password
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        # We override update to hash the password if it is being changed
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    # Nested serializers allow us to see the full User/Topic object (Read)
    host = UserSerializer(read_only=True)
    topic = TopicSerializer(read_only=True)
    
    # Write-only field to accept an ID when creating/updating a room
    topic_id = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all(), source='topic', write_only=True
    )

    class Meta:
        model = Room
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = '__all__'
        # We set 'room' to read_only so the serializer doesn't require it 
        # in the input (since we attach it automatically in the view)
        read_only_fields = ['room']


class ActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    room = serializers.ReadOnlyField(source='room.name') # Just get the room name

    class Meta:
        model = Message
        fields = ['id', 'user', 'room', 'body', 'created']