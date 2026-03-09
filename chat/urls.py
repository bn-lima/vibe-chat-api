from django.urls import path, include
from .views import CreateChatRoom, ChatRooms, PublicChatRooms, ChatRoomDetail, JoinChatRoom, LeaveChatRoom, MyChatRooms, DeleteChatRoom

urlpatterns = [
    path("rooms/", ChatRooms.as_view(), name="rooms"), # Lista as salas disponíveis
    path("new/", CreateChatRoom.as_view(), name="new"), # Cria uma nova sala de conversa
    path("public/", PublicChatRooms.as_view(), name="public"), # Mostra todas as salas públicas
    path("myrooms/", MyChatRooms.as_view(), name="myrooms"), # Mostra todas as salas que o usuário participa

    path("<int:pk>/", include([
        path("detail/", ChatRoomDetail.as_view(), name="detail"), # Mostra os detalhes de uma sala específica (passando seu id pra view)
        path("join/", JoinChatRoom.as_view(), name="join"), # Entra em uma sala específica (passando seu id pra view)
        path("leave/", LeaveChatRoom.as_view(), name="leave"), # Sai de uma sala específica
        path("delete/", DeleteChatRoom.as_view(), name="delete") # Deleta uma sala de conversa específica
    ])),
]