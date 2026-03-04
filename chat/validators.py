from django.core.validators import RegexValidator

CHAT_ROOM_VALIDATOR = RegexValidator(r"^\w{0,10}$")