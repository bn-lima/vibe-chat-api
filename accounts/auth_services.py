from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

def authenticate_client(email, password):
    user = authenticate(email=email, password=password)

    if not user:
        return None
    
    token, _ = Token.objects.get_or_create(user=user)
    return token
    
