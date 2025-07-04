from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from users.models import CustomUser
from celery import shared_task
from blog.models import Comment, LiveBlog


@shared_task
def notify_users_on_blog_create(blog_id):
    blog_instance = LiveBlog.objects.get(id=blog_id)
    channel_layer = get_channel_layer()
    message = f"New blog created: {blog_instance.title}"
    
    for user in CustomUser.objects.all():
        group_name = f"user_{user.id}"
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_notification",
                "message": message,
                "message_type": "blog", 
            }
        )

@shared_task
def notify_blogger_on_comment(comment_id):
    comments = Comment.objects.get(id=comment_id)
    blog = comments.blog
    print('blog : ', blog)
    blog_author = blog.author
    print('blog_author : ', blog_author)
    current_user = comments.user
    print('current user : ', current_user)

    if current_user == blog_author:
        print("commented on own post")
        return 

    message = f"{current_user.username} commented on your blog '{blog.title}': {comments.content}"
    
    channel_layer = get_channel_layer()
    group_name = f"user_{blog_author.id}"

    print(message)
    print(group_name)
    

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "send_notification",
            "message": message,
            # "blog_id": blog.id,
            # "message_type": "comment"
        }
    )