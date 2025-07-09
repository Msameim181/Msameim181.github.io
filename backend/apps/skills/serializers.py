from rest_framework import serializers
from apps.skills.models import SkillCategory, Skill


class SkillSerializer(serializers.ModelSerializer):
    """
    Serializer for Skill model.
    """
    class Meta:
        model = Skill
        fields = [
            'id', 'name', 'category', 'proficiency', 'icon',
            'order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class SkillCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for SkillCategory model.
    """
    skills = SkillSerializer(many=True, read_only=True)
    
    class Meta:
        model = SkillCategory
        fields = [
            'id', 'name', 'order', 'skills',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
