from rest_framework.views import APIView
from rest_framework import permissions
from .serializers import ChatRoomSerializers
from rest_framework.response import Response

class CreateChatRoom(APIView): # Cria uma nova sala de conversa
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        serializer = ChatRoomSerializers(data=request.data, context={"user": user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Your channel has created successfully"})