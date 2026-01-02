from rest_framework import serializers
from base.models import Room, Topic, Message, Friendship
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

# --- NEW SERIALIZER ---
class FriendSerializer(serializers.ModelSerializer):
    friend = UserSerializer(read_only=True)
    
    class Meta:
        model = Friendship
        fields = ['id', 'friend', 'created']

class RoomSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    topic = TopicSerializer(read_only=True)
    
    # Topic Handling
    topic_id = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all(), 
        source='topic', 
        write_only=True, 
        required=False, 
        allow_null=True
    )
    topic_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Room
        fields = '__all__'

    def create(self, validated_data):
        # Handle Topic Creation
        topic_name = validated_data.pop('topic_name', None)
        if topic_name:
            topic, created = Topic.objects.get_or_create(name=topic_name)
            validated_data['topic'] = topic

        return super().create(validated_data)

    def update(self, instance, validated_data):
        topic_name = validated_data.pop('topic_name', None)
        if topic_name:
            topic, created = Topic.objects.get_or_create(name=topic_name)
            instance.topic = topic
            
        return super().update(instance, validated_data)

class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['room']

class ActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    room = serializers.ReadOnlyField(source='room.name')
    topic = serializers.ReadOnlyField(source='room.topic.name')

    class Meta:
        model = Message
        fields = ['id', 'user', 'room', 'topic', 'body', 'created']