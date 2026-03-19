from django.contrib import admin
from .models import ChatRoom, ChatMessage

class MessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 1

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    search_fields = ("owner", "channel_name", "created_at", "subject")
    list_display = ("owner", "channel_name", "created_at", "subject")
    inlines = [MessageInline]