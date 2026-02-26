from rest_framework import serializers
from .models import ChatRoom

class ChatRoomSerializers(serializers.ModelSerializer):
    
    class Meta():
        model = ChatRoom
        exclude = ("members", "created_at", "owner")

    def create(self, validated_data):
        password = validated_data.get("password")
        user = self.context.get("user")

        chat_room = ChatRoom.objects.create( # Cria uma sala de conversa passando o usuário logado e outras informações
            owner=user,
            channel_name=validated_data.get("channel_name"),
            password=password if password else None,
            subject=validated_data.get('subject')
        )

        return chat_room