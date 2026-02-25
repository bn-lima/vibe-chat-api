from rest_framework import serializers
from .models import Account, ResetToken
from .auth_services import authenticate_client, has_many_reset_tokens, logout_user
from .email import send_reset_token_by_email
class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True, max_length=128, min_length=8)
    password = serializers.CharField(required=True, max_length=128, min_length=8)
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
    password = serializers.CharField(required=True, max_length=128, min_length=8)

    def validate(self, data):
        email = data['email']
        password = data['password']

        token = authenticate_client(email, password)

        if not token:
            raise serializers.ValidationError("Invalid email or password")
        data['token'] = token

        return data
    
    def save(self, **kwargs):
        token = self.validated_data.get('token')
        return token
    
class ChangePasswordRequestSerializer(serializers.Serializer):

    def validate(self, data):
        user = self.context.get('user')

        if has_many_reset_tokens(user):
            raise serializers.ValidationError("You have too many active reset tokens. Please click the link sent to your email or wait one hour")
    
        return data
    
    def save(self, **kwargs):
        user = self.context.get('user')

        reset_token = ResetToken.objects.create(user=user)

        send_reset_token_by_email(user.email, reset_token.key)
        
class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, max_length=128, min_length=8)
    confirm_new_password = serializers.CharField(required=True, max_length=128, min_length=8)

    def validate(self, data):

        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("Passwords do not match")
        
        user = self.context.get('user')

        if user.check_password(data['new_password']):
            raise serializers.ValidationError("The new password cannot be the same as your current password")
        
        return data
    
    def save(self, **kwargs):
        user = self.context.get('user')

        user.set_password(self.validated_data.get('new_password'))
        user.save()

        logout_user(user)

        ResetToken.objects.filter(user=user, active=True).update(active=False)

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, max_length=254)

    def validate(self, data):
        email = data['email']

        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            raise serializers.ValidationError("Invalid email")
        
        if has_many_reset_tokens(user):
            raise serializers.ValidationError("You have too many active reset tokens. Please click the link sent to your email or wait one hour")
        
        data['user'] = user
        return data
    
    def save(self, **kwargs):
        user = self.validated_data.get('user')

        reset_token = ResetToken.objects.create(user=user)

        send_reset_token_by_email(user.email, reset_token.key)