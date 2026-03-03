from rest_framework.views import APIView
from rest_framework import permissions
from .serializers import ChatRoomSerializers, ChatRoomsSerializer
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .pagination import ChatRoomsPagination
from .models import ChatRoom
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank

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

    def get_queryset(self):
        query_params = self.request.query_params.get("search")

        if query_params:

            search_vector = SearchVector("channel_name", weight="A") + SearchVector("subject", weight="B")  # Aplica full-text search priorizando o nome da sala sobre o assunto

            search_query = SearchQuery(query_params) # Converte o termo pesquisado em uma consulta compatível com o mecanismo de busca do PostgreSQL

            queryset = self.queryset.annotate(rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.1).order_by("-rank") # Retorna apenas resultados com relevância mínima e ordena do mais relevante para o menos relevante

            return queryset
        return self.queryset