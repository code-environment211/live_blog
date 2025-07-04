from django.urls import path
from Notifications.consumers import NotificationConsumer

websocket_urlpatterns = [
    path("ws/blog-notifications/", NotificationConsumer.as_asgi()),
]