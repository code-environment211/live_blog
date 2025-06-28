from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return self.username

class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='my_followers', on_delete=models.CASCADE) 
    following = models.ForeignKey(CustomUser, related_name='i_follow', on_delete=models.CASCADE)

    class Meta:
        unique_together =('follower', 'following')

    def __str__(self):
        return f"{self.follower} follows {self.following}"
    
