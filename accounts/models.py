from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from datetime import timedelta
from django.utils import timezone
class Account(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)
    discriminator = models.CharField(max_length=5)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =  ('username',)

    def save(self, *args, **kwargs):
        from .auth_services import create_discriminator

        if not self.discriminator:
            self.discriminator = create_discriminator(str(self.username))
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username}#{self.discriminator} - {self.email}"
    
class ResetToken(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    key = models.UUIDField(default=uuid.uuid4)
    expiration = models.DateTimeField()
    active = models.BooleanField(default=True)  

    def save(self, *args, **kwargs):
        if not self.expiration:
            self.expiration = timezone.now() + timedelta(minutes=60)
        return super().save(*args, **kwargs)
    
    def is_token_expired(self):
        return self.expiration < timezone.now()
    
    def mark_token_as_expired(self):
        self.active = False
        self.save()

    def __str__(self):
        return f"{self.key}"