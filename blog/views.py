from rest_framework import viewsets, permissions, filters
from .models import LiveBlog, Comment
from .serializers import LiveBlogSerializer, CommentSerializer
from django.shortcuts import render
from users.models import CustomUser

class LiveBlogViewSet(viewsets.ModelViewSet):
    queryset = LiveBlog.objects.all().order_by('-timestamp')
    serializer_class = LiveBlogSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content', 'event_status']

    def perform_create(self, serializer):
        blog = serializer.save(author=self.request.user)
        notify_users_on_blog_create(blog)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['content']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
# ------------------------------------------------------------------------------------------------------------------------------------------------

# webpage view : 
def homepage(request):
    return render(request, 'index.html')


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify_users_on_blog_create(blog_instance):
    channel_layer = get_channel_layer()
    message = f"New blog created: {blog_instance.title}"
    
    for user in CustomUser.objects.all():
        group_name = f"user_{user.id}"
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_notification",
                "message": message
            }
        )
