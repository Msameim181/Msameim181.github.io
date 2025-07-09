from rest_framework import serializers
from apps.resume.models import Education, Experience


class EducationSerializer(serializers.ModelSerializer):
    """
    Serializer for Education model.
    """
    class Meta:
        model = Education
        fields = [
            'id', 'institution', 'degree', 'field_of_study', 'start_date', 
            'end_date', 'description', 'location', 'is_current', 
            'order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ExperienceSerializer(serializers.ModelSerializer):
    """
    Serializer for Experience model.
    """
    class Meta:
        model = Experience
        fields = [
            'id', 'company', 'position', 'start_date', 'end_date',
            'description', 'location', 'is_current', 'order',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
