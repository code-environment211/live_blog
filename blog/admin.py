from django.contrib import admin
from .models import LiveBlog, Comment

# Register your models here.
admin.site.register(LiveBlog)
admin.site.register(Comment)

