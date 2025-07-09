import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.profile.models import Profile
from apps.profile.serializers import ProfileSerializer


@pytest.mark.django_db
class TestProfileSerializer:
    """
    Tests for the ProfileSerializer.
    """
    def test_profile_serialization(self):
        """Test that a profile is serialized correctly."""
        profile = Profile.objects.create(
            first_name="John",
            last_name="Doe",
            title="Software Developer",
            bio="Test bio",
            email="john@example.com",
            location="New York"
        )
        
        serializer = ProfileSerializer(profile)
        data = serializer.data
        
        assert data['id'] == profile.id
        assert data['first_name'] == "John"
        assert data['last_name'] == "Doe"
        assert data['full_name'] == "John Doe"
        assert data['title'] == "Software Developer"
        assert data['bio'] == "Test bio"
        assert data['email'] == "john@example.com"
        assert data['location'] == "New York"
    
    def test_profile_deserialization(self):
        """Test that a profile can be deserialized."""
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'title': 'UX Designer',
            'bio': 'Test bio for Jane',
            'email': 'jane@example.com',
            'location': 'San Francisco'
        }
        
        serializer = ProfileSerializer(data=data)
        assert serializer.is_valid()
        
        profile = serializer.save()
        assert profile.first_name == 'Jane'
        assert profile.last_name == 'Doe'
        assert profile.title == 'UX Designer'
