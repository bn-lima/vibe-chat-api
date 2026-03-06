from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import ResetToken
import uuid
from . models import Account
import random

def authenticate_client(email, password):
    user = authenticate(email=email, password=password)

    if not user:
        return None
    
    token, _ = Token.objects.get_or_create(user=user)
    return token
    
def logout_user(user):
    Token.objects.filter(user=user).delete()

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

def username_has_discriminator(username, discriminator):
    users = Account.objects.filter(username=username)

    for account in users:
        if account.discriminator == discriminator:
            return True
        
    return False

def create_discriminator(username):

    while True:

        discriminator = ""

        for i in range(0,4):
            discriminator = str(random.randint(0,9)) + discriminator

        if username_has_discriminator(username, discriminator):
            continue

        return f"#{discriminator}"