from django.db import models
from accounts.models import Account

class Profile(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="profile", default="profile/default.jpg")
    description = models.CharField(max_length=500, blank=True)
    display_name = models.CharField(max_length=150, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birthday = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.display_name or self.account.username}"