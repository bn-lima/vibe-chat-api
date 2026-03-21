from rest_framework.generics import RetrieveAPIView
from .models import Profile
from rest_framework import permissions
from .serializers import ProfileDetailSerializer

class ProfileDetail(RetrieveAPIView):
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileDetailSerializer