from rest_framework.views import APIView
from rest_framework import permissions
from .serializers import ChatRoomSerializers, ChatRoomsSerializer
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .pagination import ChatRoomsPagination
from .models import ChatRoom

class CreateChatRoom(APIView): # Cria uma nova sala de conversa
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        serializer = ChatRoomSerializers(data=request.data, context={"user": user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Your channel has created successfully"})

class ChatRooms(ListAPIView): #Mostra todas as salas de conversa disponíveis
    queryset = ChatRoom.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatRoomsSerializer
    pagination_class = ChatRoomsPagination