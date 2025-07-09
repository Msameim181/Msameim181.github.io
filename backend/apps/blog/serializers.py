from rest_framework import serializers
from apps.blog.models import Category, Tag, Post


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'posts_count']
    
    def get_posts_count(self, obj):
        return obj.posts.filter(status='published').count()


class PostListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    cover_image_url = serializers.SerializerMethodField()
    cover_thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'subtitle', 'excerpt',
            'category', 'category_name', 'category_slug',
            'tags', 'cover_image_url', 'cover_thumbnail_url',
            'published_at', 'featured'
        ]

    def get_cover_image_url(self, obj):
        if obj.cover_image:
            return obj.cover_image.url
        return None

    def get_cover_thumbnail_url(self, obj):
        if obj.cover_image:
            return obj.cover_image_thumbnail.url
        return None


class PostDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    cover_image_url = serializers.SerializerMethodField()
    cover_thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'subtitle', 'content', 'excerpt',
            'category', 'category_name', 'category_slug',
            'tags', 'cover_image_url', 'cover_thumbnail_url',
            'published_at', 'featured', 'created_at', 'updated_at'
        ]

    def get_cover_image_url(self, obj):
        if obj.cover_image:
            return obj.cover_image.url
        return None

    def get_cover_thumbnail_url(self, obj):
        if obj.cover_image:
            return obj.cover_image_thumbnail.url
        return None
