from django.conf import settings
from rest_framework import serializers
from users.serializers import PublicUserProfileSerializer
from .models import Node

MAX_NODE_LENGTH = settings.MAX_NODE_LENGTH
NODE_ACTION_OPTIONS = settings.NODE_ACTION_OPTIONS


class NodeActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in NODE_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for nodes")
        return value


class NodeCreateSerializer(serializers.ModelSerializer):
    user = PublicUserProfileSerializer(source='user.userprofile', read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Node
        fields = ['user', 'id', 'content', 'likes', 'comments', 'timestamp']
    
    def get_likes(self, obj):
        return obj.likes.count()
    
    def get_comments(self, obj):
        return obj.comments.count()

    def validate_content(self, value):
        if len(value) > MAX_NODE_LENGTH:
            raise serializers.ValidationError("This node is too long")
        return value


class NodeSerializer(serializers.ModelSerializer):
    user = PublicUserProfileSerializer(source='user.userprofile', read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    parent = NodeCreateSerializer(read_only=True)

    class Meta:
        model = Node
        fields = [
                'user', 
                'id', 
                'content',
                'likes',
                'comments',
                'is_repost',
                'parent',
                'timestamp',
                ]

    def get_likes(self, obj):
        return obj.likes.count()

    def get_comments(self, obj):
        return obj.comments.count()
        