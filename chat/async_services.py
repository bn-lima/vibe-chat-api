from channels.db import database_sync_to_async
from .chat_services import get_chat_room_by_id
from rest_framework.authtoken.models import Token

@database_sync_to_async
def is_user_in_room(user, id):
    room = get_chat_room_by_id(id)

    if not room:
        return False

    if not room.members.filter(id=user.id).exists():
        return False
    return True

@database_sync_to_async
def get_user_by_auth_token(token): # Verifica se existe um usuário associado a esse token
    try:
        token = Token.objects.get(key=token)
    except Token.DoesNotExist:
        return None
    return token.user