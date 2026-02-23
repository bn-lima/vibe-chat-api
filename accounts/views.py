from rest_framework.views import APIView
from rest_framework import permissions, status
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from .auth_services import logout_user

class Register(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Your account has been created sucessfully"}, status=status.HTTP_201_CREATED)

class Login(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, required=False)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()

        return Response({"auth_token": token.key})
    
class Logout(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        logout_user(request.user)

        return Response({"detail": "The logout was sucessfully"}, status=status.HTTP_204_NO_CONTENT)