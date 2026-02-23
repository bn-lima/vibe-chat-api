from django.db import models
from django.contrib.auth.models import AbstractUser

class Account(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =  ('username',)

    def __str__(self):
        return f"{self.username} - {self.email}"