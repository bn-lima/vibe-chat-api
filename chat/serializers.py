from rest_framework import serializers
from .models import ChatRoom, ChatMessage
from .validators import CHAT_ROOM_VALIDATOR

class CreateChatRoomSerializer(serializers.ModelSerializer):
    class Meta():
        model = ChatRoom
        exclude = ("members", "created_at", "owner")

    def create(self, validated_data):
        password = validated_data.get("room_password")
        user = self.context.get("user")

        chat_room = ChatRoom.objects.create( # Cria uma sala de conversa passando o usuário logado e outras informações
            owner=user,
            channel_name=validated_data.get("channel_name"),
            room_password=password if password else None,
            subject=validated_data.get('subject')
        )

        chat_room.members.add(chat_room.owner)

        return chat_room
    
class ChatRoomsSerializer(serializers.ModelSerializer): # Serializer responsável por retornar os dados da sala e a quantidade total de participantes
    members_quantity = serializers.SerializerMethodField()
    class Meta():
        model = ChatRoom
        exclude = ["owner", "room_password", "members"]

    def get_members_quantity(self, obj):
        return obj.members.count() # Número de membros da sala
    
class ChatRoomDetailSerializer(serializers.ModelSerializer):
    owner_name = serializers.SerializerMethodField()
    owner_display_name = serializers.SerializerMethodField()
    members_quantity = serializers.SerializerMethodField()
    class Meta:
        model = ChatRoom
        exclude = ("room_password", "owner", "members")

    def get_owner_name(self, obj):
        return f"{obj.owner.username}{obj.owner.discriminator}"
    
    def get_members_quantity(self, obj):    
        return obj.members.count()
    
    def get_owner_display_name(self, obj):
        return obj.owner.profile.display_name
    
class JoinChatRoomSerializer(serializers.Serializer): # Serializer responsável por verificar se a senha da sala está correta e permitir a entrada do usuário
    room_password = serializers.CharField(max_length=10, validators=[CHAT_ROOM_VALIDATOR], required=False)

    def validate(self, data):
        chat_room = self.context.get("chat_room")

        if chat_room.room_password and data["room_password"] != chat_room.room_password:
            raise serializers.ValidationError("Invalid password")

        return data
     
    def save(self, **kwargs):
        user = self.context.get("user")
        chat_room = self.context.get("chat_room")

        chat_room.members.add(user)

class LeaveChatRoomSerializer(serializers.Serializer): # Serializer responsável por remover o usuário da sala de conversa

    def validate(self, data):
        user = self.context.get("user")
        chat_room = self.context.get("chat_room")

        if chat_room.owner == user: # Verifica se o usuário é o dono da sala
            raise serializers.ValidationError("You cannot leave your own room")
        
        return data

    def save(self, **kwargs):
        user = self.context.get("user")
        chat_room = self.context.get("chat_room")

        chat_room.members.remove(user) # Remove o usuário da sala

class DeleteChatRoomSerializer(serializers.Serializer):
    delete_confirmation = serializers.CharField(max_length=100, required=True) # Permite que o usuário prossiga com a exclusão da sala de conversa ao digitar o nome exato da sala

    def validate(self, data):
        delete_confirmation = data['delete_confirmation']
        chat_room = self.context.get("chat_room")
        user = self.context.get("user")
        
        if chat_room.owner != user: # Verifica se o usuário logado é o dono da sala
            raise serializers.ValidationError("You are not the owner of this chat room")

        if delete_confirmation != chat_room.channel_name: # verifica se o a confirmação de exclusão é válida
            raise serializers.ValidationError({"delete_confirmation": "Type the correct name of the chat room if you want to delete it"})
        
        return data
    
class MessagesSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField() # Mostra o username do usuário junto das suas mensagens
    class Meta:
        model = ChatMessage
        exclude = ("channel",)

    def get_username(self, obj):
        return f"{obj.author.profile.display_name or obj.author.username}"
class ShowChatRoomSerializer(serializers.ModelSerializer): # Serializer responsável por mostrar a sala com todas as mensagens
    messages = MessagesSerializer(many=True, read_only=True) # Usa o serializer MessagesSerializer como campo para mostrar as mensagens da sala
    class Meta:
        model = ChatRoom
        fields = ("channel_name", "messages",)

class SendMessageSerializer(serializers.ModelSerializer): # Serializer responsável por criar um objeto mensagem em uma sala específica
    message_content = serializers.CharField(max_length=1000, required=False)
    class Meta:
        model = ChatMessage
        exclude = ("channel", "author",)
    
    def create(self, validated_data):
        user = self.context.get("user")
        chat_room = self.context.get("chat_room")

        message = ChatMessage.objects.create( # Cria a mensagem na sala e define o usuário logado como autor
            author=user,
            channel=chat_room,
            **validated_data
        )

        return message