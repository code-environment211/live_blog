import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

class NotificationConsumer(AsyncWebsocketConsumer):
    group_name = None
    async def connect(self):
        user = self.scope["user"]
        print("WebSocket connection attempt by user:", self.scope["user"])

        if isinstance(user, AnonymousUser) or not user.is_authenticated:
            await self.close()
        else:
            self.group_name = f"user_{user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            

    async def disconnect(self, close_code):
        if self.group_name:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
    
    async def receive(self, text_data):
        print(text_data)
        pass

    async def send_notification(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({
            "message": event["message"],
            # "message_type": event.get("message_type", "info"),
            # "blog_id": event.get("blog_id"),
            }))
        



