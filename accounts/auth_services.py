from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import ResetToken
import uuid

def authenticate_client(email, password):
    user = authenticate(email=email, password=password)

    if not user:
        return None
    
    token, _ = Token.objects.get_or_create(user=user)
    return token
    
def logout_user(user):
    token = Token.objects.get(user=user)
    token.delete()

def has_many_reset_tokens(user):
    
    tokens = ResetToken.objects.filter(user=user, active=True).count()

    if tokens >= 3:
        return True
    return False

def validate_reset_token(str_reset_token):

    try:
        uuid_token = uuid.UUID(str_reset_token)
    except ValueError:
        return None
    
    try:
        reset_token = ResetToken.objects.get(key=uuid_token)
    except ResetToken.DoesNotExist:
            return None
    
    if not reset_token.active:
        return None
    
    return reset_token