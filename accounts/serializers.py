from rest_framework import serializers
from .models import Account

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True, max_length=150)

    class Meta:
        model = Account
        fields = ('username', 'email', 'password', 'confirm_password')

    def validate(self, data):
        password = data['password']
        confirm_password = data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")
        
        data.pop('confirm_password', None)
        return data
    
    def save(self, **kwargs):
        password = self.validated_data.pop('password')

        user = Account.objects.create(
            **self.validated_data
        )

        user.set_password(password)
        user.save()
        
        return user