from rest_framework import serializers
from apps.profile.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile model.
    """
    class Meta:
        model = Profile
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'title', 'bio', 'avatar',
            'email', 'phone', 'location', 'github', 'linkedin',
            'twitter', 'website', 'created_at', 'updated_at'
        ]
        read_only_fields = ['full_name', 'created_at', 'updated_at']
