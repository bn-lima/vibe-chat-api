from django.db import models
from accounts.models import Account

class ChatRoom(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="channels")
    channel_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(Account, related_name="joined_channels")
    room_password = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.channel_name} ({self.subject}) - {self.owner}"
    
class ChatMessage(models.Model):
    channel = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    message_content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message_content} - {self.channel.channel_name}"
