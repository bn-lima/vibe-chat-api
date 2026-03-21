from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("photo", "display_name", "description", "location", "birthday", "account")
    search_fields = ("photo", "display_name", "description", "location", "birthday", "account")