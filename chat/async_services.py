from channels.db import database_sync_to_async
from .chat_services import get_chat_room_by_id

@database_sync_to_async
def is_user_in_room(user, id):
    room = get_chat_room_by_id(id)

    if not room.members.filter(id=user.id).exists():
        return False
    return True