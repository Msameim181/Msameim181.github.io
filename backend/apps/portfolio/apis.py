from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.portfolio.models import ProjectCategory, Project, ProjectImage
from apps.portfolio.serializers import (
    ProjectCategorySerializer,
    ProjectCategoryDetailSerializer,
    ProjectListSerializer,
    ProjectDetailSerializer,
    ProjectImageSerializer
)


class ProjectCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProjectCategory.objects.all()
    serializer_class = ProjectCategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectCategoryDetailSerializer
        return ProjectCategorySerializer

    @action(detail=True, methods=['get'])
    def projects(self, request, slug=None):
        """
        Return all projects for a specific category
        """
        category = self.get_object()
        projects = Project.objects.filter(category=category)
        
        serializer = ProjectListSerializer(projects, many=True)
        return Response(serializer.data)


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by category slug if provided
        category_slug = self.request.query_params.get('category', None)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Filter featured projects
        featured = self.request.query_params.get('featured', None)
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
            
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectListSerializer

    @action(detail=True, methods=['get'])
    def images(self, request, slug=None):
        """
        Return all images for a specific project
        """
        project = self.get_object()
        images = project.images.all()
        
        serializer = ProjectImageSerializer(images, many=True)
        return Response(serializer.data)
