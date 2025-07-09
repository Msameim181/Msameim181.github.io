from rest_framework import serializers
from apps.portfolio.models import ProjectCategory, Project, ProjectImage


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'image_thumbnail', 'caption', 'is_cover', 'order']


class ProjectListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'category', 'category_name',
            'description', 'technologies', 'start_date', 'end_date',
            'cover_image', 'is_featured', 'order'
        ]

    def get_cover_image(self, obj):
        if obj.cover_image:
            return {
                'full': obj.cover_image.url,
                'thumbnail': obj.cover_image_thumbnail.url if obj.cover_image else None
            }
        
        cover_image = obj.images.filter(is_cover=True).first()
        if cover_image:
            return {
                'full': cover_image.image.url,
                'thumbnail': cover_image.image_thumbnail.url
            }
        return None


class ProjectDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    images = ProjectImageSerializer(many=True, read_only=True)
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'category', 'category_name', 'client',
            'description', 'content', 'technologies', 'start_date', 'end_date',
            'website_url', 'github_url', 'cover_image', 'images',
            'is_featured', 'order', 'created_at', 'updated_at'
        ]

    def get_cover_image(self, obj):
        if obj.cover_image:
            return {
                'full': obj.cover_image.url,
                'thumbnail': obj.cover_image_thumbnail.url if obj.cover_image else None
            }
        
        cover_image = obj.images.filter(is_cover=True).first()
        if cover_image:
            return {
                'full': cover_image.image.url,
                'thumbnail': cover_image.image_thumbnail.url
            }
        return None


class ProjectCategorySerializer(serializers.ModelSerializer):
    projects_count = serializers.SerializerMethodField()

    class Meta:
        model = ProjectCategory
        fields = ['id', 'name', 'slug', 'description', 'order', 'projects_count']
    
    def get_projects_count(self, obj):
        return obj.projects.count()


class ProjectCategoryDetailSerializer(serializers.ModelSerializer):
    projects = ProjectListSerializer(many=True, read_only=True)

    class Meta:
        model = ProjectCategory
        fields = ['id', 'name', 'slug', 'description', 'order', 'projects']
