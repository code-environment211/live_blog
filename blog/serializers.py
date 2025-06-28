from rest_framework import serializers
from .models import LiveBlog, Comment

class LiveBlogSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = LiveBlog
        fields = ['id', 'title', 'content', 'author', 'timestamp', 'event_status']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'blog', 'user', 'content', 'created_at']