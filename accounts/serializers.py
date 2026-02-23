from rest_framework import serializers
from .models import Account
from .auth_services import authenticate_client

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
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=254)
    password = serializers.CharField(required=True, max_length=128)

    def validate(self, data):
        email = data['email']
        password = data['password']

        token = authenticate_client(email, password)

        if not token:
            raise serializers.ValidationError("Invalid email or user not found")
        data['token'] = token

        return data
    
    def save(self, **kwargs):
        token = self.validated_data.get('token')
        return token