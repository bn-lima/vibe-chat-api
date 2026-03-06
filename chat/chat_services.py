from .models import ChatRoom

def get_chat_room_by_id(id):
    try:
        chat_room = ChatRoom.objects.get(id=id)
    except ChatRoom.DoesNotExist:
        return None
    return chat_room
    
def is_user_in_room(user, chat_room):
    try:
        ChatRoom.objects.get(id=chat_room.id, members__id=user.id)
    except ChatRoom.DoesNotExist:
        return False
    return True