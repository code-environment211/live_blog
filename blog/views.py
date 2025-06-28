from rest_framework import viewsets, permissions, filters
from .models import LiveBlog, Comment
from .serializers import LiveBlogSerializer, CommentSerializer

class LiveBlogViewSet(viewsets.ModelViewSet):
    queryset = LiveBlog.objects.all().order_by('-timestamp')
    serializer_class = LiveBlogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content', 'event_status']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['content']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)