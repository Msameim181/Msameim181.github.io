from rest_framework import viewsets
from apps.profile.models import Profile
from apps.profile.serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows profiles to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
