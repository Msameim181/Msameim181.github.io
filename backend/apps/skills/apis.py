from rest_framework import viewsets
from apps.skills.models import SkillCategory, Skill
from apps.skills.serializers import SkillCategorySerializer, SkillSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class SkillCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows skill categories to be viewed or edited.
    """
    queryset = SkillCategory.objects.all()
    serializer_class = SkillCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    ordering_fields = ['order']


class SkillViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows skills to be viewed or edited.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['category']
    ordering_fields = ['order', 'proficiency']
