from rest_framework import serializers
from .models import Profile
class ProfileDetailSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        exclude = ("account",)

    def get_username(self, obj):
        return f"{obj.account.username}{obj.account.discriminator}"
    
class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ("account",)

    def save(self, **kwargs):
        profile = self.instance

        for key, value in self.validated_data.items():
            setattr(profile, key, value)

        profile.save()
        return profile