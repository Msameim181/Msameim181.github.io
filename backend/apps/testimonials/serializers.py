from rest_framework import serializers
from apps.testimonials.models import Testimonial


class TestimonialSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    avatar_thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Testimonial
        fields = [
            'id', 'name', 'position', 'company', 'content',
            'rating', 'is_featured', 'avatar_url', 'avatar_thumbnail_url',
            'created_at'
        ]

    def get_avatar_url(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None

    def get_avatar_thumbnail_url(self, obj):
        if obj.avatar:
            return obj.avatar_thumbnail.url
        return None
