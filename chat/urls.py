from django.urls import path, include
from .views import CreateChatRoom, ChatRooms, PublicChatRooms

urlpatterns = [
    path("new/", CreateChatRoom.as_view(), name="new"), # Cria uma nova sala de conversa
    path("rooms/", ChatRooms.as_view(), name="rooms"), # Lista as salas disponíveis
    path("public/", PublicChatRooms.as_view(), name="public")
]