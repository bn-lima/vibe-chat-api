from rest_framework.views import APIView
from rest_framework import permissions, status
from .serializers import RegisterSerializer, LoginSerializer, ChangePasswordRequestSerializer, ChangePasswordSerializer, ForgotPasswordSerializer
from rest_framework.response import Response
from .auth_services import logout_user, validate_reset_token

class Register(APIView): # Cria um novo usuário
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Your account has been created sucessfully"}, status=status.HTTP_201_CREATED)

class Login(APIView): # Autentica usuário e retorna token
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()

        return Response({"auth_token": token.key})
    
class Logout(APIView): # Logout do usuário, removendo o token
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        logout_user(request.user)

        return Response({"detail": "The logout was sucessfully"}, status=status.HTTP_204_NO_CONTENT)
    
class ChangePasswordRequest(APIView): # Gera token de reset de senha para usuário logado
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        serializer = ChangePasswordRequestSerializer(data={}, context={'user':user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "An email with a reset link has been sent to you"}, status=status.HTTP_200_OK)
    
class ChangePassword(APIView): # Altera a senha usando token de reset
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        
        str_reset_token = request.query_params.get('reset_token')

        if not str_reset_token:
            return Response({"detail": "Reset token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        reset_token = validate_reset_token(str_reset_token)

        if not reset_token:
            return Response({"detail": "Invalid or expired reset token"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = reset_token.user

        serializer = ChangePasswordSerializer(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Your password has been updated successfully"}, status=status.HTTP_200_OK)
    
class ForgotPassword(APIView): # Solicita reset de senha via email (usuário não logado)
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):

        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "An email with a reset link has been sent to you"}, status=status.HTTP_200_OK)
