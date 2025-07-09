from rest_framework import viewsets
from apps.resume.models import Education, Experience
from apps.resume.serializers import EducationSerializer, ExperienceSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class EducationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows education entries to be viewed or edited.
    """
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['is_current']
    ordering_fields = ['order', 'start_date', 'end_date']


class ExperienceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows experience entries to be viewed or edited.
    """
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['is_current']
    ordering_fields = ['order', 'start_date', 'end_date']
