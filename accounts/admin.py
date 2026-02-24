from django.contrib import admin
from .models import Account, ResetToken

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['username', 'email',]
    search_fields = ['username', 'email',]

@admin.register(ResetToken)
class ResetTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'key', 'expiration', 'active']
    search_fields = ['user', 'key', 'expiration', 'active']
    readonly_fields = ['key', 'user']