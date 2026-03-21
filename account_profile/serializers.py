from rest_framework import serializers
from .models import Profile
class ProfileDetailSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        exclude = ("account",)

    def get_username(self, obj):
        return f"{obj.account.username}{obj.account.discriminator}"