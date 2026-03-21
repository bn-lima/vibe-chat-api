from rest_framework.generics import RetrieveAPIView
from .models import Profile
from rest_framework import permissions, status
from .serializers import ProfileDetailSerializer, EditProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
class ProfileDetail(RetrieveAPIView):
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileDetailSerializer

class EditProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        profile = Profile.objects.get(account=user)

        serializer = EditProfileSerializer(instance=profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)