# from django.shortcuts import render
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# from users.models import CustomUser

# class Notification_view:

#     @staticmethod
#     def notify_users_on_blog_create(blog_instance):
#         channel_layer = get_channel_layer()
#         message = f"New blog created: {blog_instance.title}"
        
#         for user in CustomUser.objects.all():
#             group_name = f"user_{user.id}"
#             async_to_sync(channel_layer.group_send)(
#                 group_name,
#                 {
#                     "type": "send_notification",
#                     "message": message,
#                     "message_type": "blog", 
#                 }
#             )

#     @staticmethod
#     def notify_blogger_on_comment(comment):
#         blog = comment.blog
#         print('blog : ', blog)
#         blog_author = blog.author
#         print('blog_author : ', blog_author)
#         current_user = comment.user
#         print('current user : ', current_user)

#         if current_user == blog_author:
#             print("commented on own post")
#             return 

#         message = f"{current_user.username} commented on your blog '{blog.title}': {comment.content}"
        
#         channel_layer = get_channel_layer()
#         group_name = f"user_{blog_author.id}"

#         print(message)
#         print(group_name)
        

#         async_to_sync(channel_layer.group_send)(
#             group_name,
#             {
#                 "type": "send_notification",
#                 "message": message,
#                 # "blog_id": blog.id,
#                 # "message_type": "comment"
#             }
#         )