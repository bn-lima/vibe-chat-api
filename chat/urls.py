from django.urls import path, include
from .views import CreateChatRoom, ChatRooms, PublicChatRooms, ChatRoomDetail, JoinChatRoom

urlpatterns = [
    path("new/", CreateChatRoom.as_view(), name="new"), # Cria uma nova sala de conversa
    path("rooms/", ChatRooms.as_view(), name="rooms"), # Lista as salas disponíveis
    path("public/", PublicChatRooms.as_view(), name="public"), # Mostra todas as salas públicas

    path("<int:pk>/", include([
        path("detail/", ChatRoomDetail.as_view(), name="detail"), # Mostra os detalhes de uma sala expecífica (passando seu id pra view)
        path("join/", JoinChatRoom.as_view(), name="join") # Entra em uma sala expecífica (passando seu id pra view)
    ])),
]