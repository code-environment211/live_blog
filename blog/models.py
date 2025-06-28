from django.db import models
from django.conf import settings

class LiveBlog(models.Model):
    STATUS_CHOICES = (
        ('Ongoing', 'Ongoing'),
        ('Ended', 'Ended'),
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    event_status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(LiveBlog, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.blog.title}"
