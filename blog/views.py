from rest_framework import viewsets, permissions, filters
from .models import LiveBlog, Comment
from .serializers import LiveBlogSerializer, CommentSerializer
from django.shortcuts import render
from users.models import CustomUser
from Notifications.tasks import notify_blogger_on_comment, notify_users_on_blog_create

class LiveBlogViewSet(viewsets.ModelViewSet):
    queryset = LiveBlog.objects.all().order_by('-timestamp')
    serializer_class = LiveBlogSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content', 'event_status']

    def perform_create(self, serializer):
        blog = serializer.save(author=self.request.user)
        notify_users_on_blog_create.delay(blog.id)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['content']

    def perform_create(self, serializer):
        comment = serializer.save(user=self.request.user)
        notify_blogger_on_comment.delay(comment.id)

# ------------------------------------------------------------------------------------------------------------------------------------------------

# webpage view : 
def homepage(request):
    return render(request, 'index.html')


######devanshu
def nothing(request):
    return 

def nothingnew(request):
    return 