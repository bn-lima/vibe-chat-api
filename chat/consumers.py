from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .async_services import is_user_in_room

class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self,):
        
        if not await is_user_in_room(self.scope["user"], self.scope["url_route"]["kwargs"]["pk"]):
            await self.close()

        self.group_name = f"chat_{self.scope['url_route']['kwargs']['pk']}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_message(self, event):
        await self.send_json(event["message"])