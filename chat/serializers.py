from rest_framework import serializers
from .models import ChatRoom

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
    members_quantity = serializers.SerializerMethodField()
    class Meta:
        model = ChatRoom
        exclude = ("room_password", "owner", "members")

    def get_owner_name(self, obj):
        return obj.owner.username
    
    def get_members_quantity(self, obj):
        return obj.members.count()