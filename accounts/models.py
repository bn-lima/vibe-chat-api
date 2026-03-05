from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from datetime import timedelta
from django.utils import timezone

class Account(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)
    username = models.EmailField(max_length=150, unique=True) # Username único para cada usuário

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =  ('username',)

    def __str__(self):
        return f"{self.username} - {self.email}" # Representação do usuário
    
class ResetToken(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE) # Usuário dono do token
    key = models.UUIDField(default=uuid.uuid4) # Chave única do token
    expiration = models.DateTimeField() # Data/hora de expiração
    active = models.BooleanField(default=True) # Token ativo ou não

    def save(self, *args, **kwargs):
        if not self.expiration:
            self.expiration = timezone.now() + timedelta(minutes=60) # Expira em 1h
        return super().save(*args, **kwargs)
    
    def is_token_expired(self):
        return self.expiration < timezone.now() # Verifica se expirou
    
    def mark_token_as_expired(self):
        self.active = False # Marca como inativo
        self.save()

    def __str__(self):
        return f"{self.key}" # Representação do token