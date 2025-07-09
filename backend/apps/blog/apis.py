from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from apps.blog.models import Category, Tag, Post
from apps.blog.serializers import (
    CategorySerializer,
    TagSerializer,
    PostListSerializer,
    PostDetailSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    @action(detail=True, methods=['get'])
    def posts(self, request, slug=None):
        """
        Return all published posts for a specific category
        """
        category = self.get_object()
        posts = Post.objects.filter(category=category, status='published')
        
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    @action(detail=True, methods=['get'])
    def posts(self, request, slug=None):
        """
        Return all published posts for a specific tag
        """
        tag = self.get_object()
        posts = Post.objects.filter(tags=tag, status='published')
        
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(status='published')
    serializer_class = PostListSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'tags__slug', 'featured']
    search_fields = ['title', 'subtitle', 'content', 'excerpt']
    ordering_fields = ['published_at', 'created_at', 'title']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostListSerializer

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Return featured posts
        """
        posts = self.queryset.filter(featured=True)
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Return most recent posts
        """
        limit = int(request.query_params.get('limit', 5))
        posts = self.queryset.order_by('-published_at')[:limit]
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)
