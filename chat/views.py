from rest_framework.views import APIView
from rest_framework import permissions, status
from .serializers import CreateChatRoomSerializer, ChatRoomsSerializer, ChatRoomDetailSerializer, JoinChatRoomSerializer, LeaveChatRoomSerializer, DeleteChatRoomSerializer, ShowChatRoomSerializer, SendMessageSerialzer
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .pagination import ChatRoomsPagination
from .models import ChatRoom
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from .chat_services import get_chat_room_by_id, is_user_in_room

class CreateChatRoom(APIView): # Cria uma nova sala de conversa
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        serializer = CreateChatRoomSerializer(data=request.data, context={"user": user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Your channel has created successfully"}, status=status.HTTP_201_CREATED)

class ChatRooms(ListAPIView): #Mostra todas as salas de conversa disponíveis
    queryset = ChatRoom.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatRoomsSerializer
    pagination_class = ChatRoomsPagination

    def get_queryset(self):
        query_params = self.request.query_params.get("search")

        if query_params:

            search_vector = SearchVector("channel_name", weight="A") + SearchVector("subject", weight="B")  # Aplica full-text search priorizando o nome da sala sobre o assunto

            search_query = SearchQuery(query_params) # Converte o termo pesquisado em uma consulta compatível com o mecanismo de busca do PostgreSQL

            queryset = self.queryset.annotate(rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.1).order_by("-rank") # Retorna apenas resultados com relevância mínima e ordena do mais relevante para o menos relevante

            return queryset
        return self.queryset
    
class PublicChatRooms(ListAPIView): # Mostra todas as salas de conversa sem senha
    queryset = ChatRoom.objects.filter(room_password=None)
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatRoomsSerializer
    pagination_class = ChatRoomsPagination
    
    def get_queryset(self):
        query_params = self.request.query_params.get("search")

        if query_params:

            search_vector = SearchVector("channel_name", weight="A") + SearchVector("subject", weight="B")

            search_query = SearchQuery(query_params)

            queryset = self.queryset.annotate(rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.1).order_by("-rank")

            return queryset
        return self.queryset
class ChatRoomDetail(RetrieveAPIView): # Mostra os detalhes de uma sala de conversa específica
    queryset = ChatRoom.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatRoomDetailSerializer

class JoinChatRoom(APIView): # Permite que o usuário entre em uma sala de conversa específica
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        user = request.user
        chat_room = get_chat_room_by_id(pk)

        if not chat_room: # Verifica se id passado realmente existe
            return Response({"detail": "Chat room not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if is_user_in_room(user, chat_room): # Verifica se o usuário já está na sala
            return Response({"detail": "You are already in this room"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = JoinChatRoomSerializer(data=request.data, context={"user":user, "chat_room":chat_room})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Successfully joined the chat."}, status=status.HTTP_200_OK)
    
class LeaveChatRoom(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        user = request.user
        chat_room = get_chat_room_by_id(pk)

        if not chat_room:
            return Response({"detail": "Chat room not found"}, status=status.HTTP_404_NOT_FOUND)

        if not is_user_in_room(user, chat_room):
            return Response({"detail": "You are not a member of this room"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = LeaveChatRoomSerializer(data={}, context={"user":user, "chat_room":chat_room})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "You left the room"}, status=status.HTTP_200_OK)
    
class MyChatRooms(ListAPIView): # Mostra uma lista de salas onde o usuário está presente
    queryset = ChatRoom.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatRoomsSerializer
    pagination_class = ChatRoomsPagination

    def get_queryset(self):
        query_params = self.request.query_params.get("search")
        user = self.request.user

        queryset = user.joined_channels.all() # Todas as salas que o usuário participa

        if query_params:

            search_vector = SearchVector("channel_name", weight="A") + SearchVector("subject", weight="B")

            search_query = SearchQuery(query_params)

            queryset = queryset.annotate(rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.1).order_by("-rank")

        return queryset
class DeleteChatRoom(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        user = request.user
        chat_room = get_chat_room_by_id(pk)

        if not chat_room:
            return Response({"detail": "Chat room not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DeleteChatRoomSerializer(data=request.data, context={"user":user, "chat_room":chat_room})
        serializer.is_valid(raise_exception=True)

        chat_room.delete() # Deleta a sala de conversa

        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ShowChatRoom(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        chat_room = get_chat_room_by_id(pk)

        if not chat_room:
            return Response({"detail": "Chat room not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ShowChatRoomSerializer(chat_room)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SendMessage(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        chat_room = get_chat_room_by_id(pk)
    
        if not chat_room:
            return Response({"detail": "Chat room not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SendMessageSerialzer(data=request.data, context={"user": request.user, "chat_room": chat_room})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_serializer = ShowChatRoomSerializer(chat_room)
        return Response(response_serializer.data)