from rest_framework.views import APIView
from rest_framework import permissions, status
from .serializers import CreateChatRoomSerializer, ChatRoomsSerializer, ChatRoomDetailSerializer, JoinChatRoomSerializer
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
class ChatRoomDetail(RetrieveAPIView): # Mostra os detalhes de uma sala de conversa expecífica
    queryset = ChatRoom.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatRoomDetailSerializer

class JoinChatRoom(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        user = request.user
        chat_room = get_chat_room_by_id(pk)

        if not chat_room:
            return Response({"detail": "Chat room not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if is_user_in_room(user, chat_room):
            return Response({"detail": "You are already in this room"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = JoinChatRoomSerializer(data=request.data, context={"user":user, "chat_room":chat_room})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Successfully joined the chat."}, status=status.HTTP_200_OK)
    