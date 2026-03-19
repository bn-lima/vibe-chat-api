from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .async_services import is_user_in_room
class ChatConsumer(AsyncJsonWebsocketConsumer): # Consumer responsável por gerenciar conexões WebSocket de uma sala de chat

    async def connect(self,):
        
        pk = self.scope["url_route"]["kwargs"]["pk"] # Obtém o id da sala a partir da URL da conexão WebSocket

        if not await is_user_in_room(self.scope["user"], pk): # Verifica se o usuário autenticado faz parte da sala
            await self.close() # Encerra a conexão caso o usuário não pertença à sala
            return

        self.group_name = f"chat_{pk}" # Define o nome do grupo usado para broadcast das mensagens

        await self.channel_layer.group_add( # Adiciona a conexão atual (usuário) ao grupo da sala
            self.group_name,
            self.channel_name
        )

        await self.accept() # Aceita a conexão WebSocket

    async def disconnect(self, close_code): # Remove a conexão do grupo quando o WebSocket é encerrado

        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def send_message(self, event): # Recebe mensagens enviadas ao grupo e envia para o cliente WebSocket
        await self.send_json(event["message"])