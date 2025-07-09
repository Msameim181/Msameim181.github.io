import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.profile.models import Profile

User = get_user_model()


@pytest.mark.django_db
class TestProfileAPI:
    """
    Tests for the Profile API endpoints.
    """
    @pytest.fixture
    def api_client(self):
        return APIClient()
    
    @pytest.fixture
    def admin_user(self):
        user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123'
        )
        return user
    
    @pytest.fixture
    def admin_client(self, admin_user):
        client = APIClient()
        client.force_authenticate(user=admin_user)
        return client
    
    @pytest.fixture
    def profile(self):
        return Profile.objects.create(
            first_name="John",
            last_name="Doe",
            title="Software Developer",
            bio="Test bio",
            email="john@example.com",
            location="New York"
        )
    
    def test_list_profiles(self, api_client, profile):
        """Test listing profiles."""
        url = reverse('profile-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
    
    def test_retrieve_profile(self, api_client, profile):
        """Test retrieving a profile."""
        url = reverse('profile-detail', kwargs={'pk': profile.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == "John"
        assert response.data['last_name'] == "Doe"
    
    def test_create_profile_unauthorized(self, api_client):
        """Test that creating a profile requires authorization."""
        url = reverse('profile-list')
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'title': 'UX Designer',
            'bio': 'Test bio for Jane',
            'email': 'jane@example.com',
            'location': 'San Francisco'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_create_profile_authorized(self, admin_client):
        """Test that an admin can create a profile."""
        url = reverse('profile-list')
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'title': 'UX Designer',
            'bio': 'Test bio for Jane',
            'email': 'jane@example.com',
            'location': 'San Francisco'
        }
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Profile.objects.count() == 1
        assert Profile.objects.first().first_name == 'Jane'
    
    def test_update_profile(self, admin_client, profile):
        """Test updating a profile."""
        url = reverse('profile-detail', kwargs={'pk': profile.pk})
        data = {
            'first_name': 'John',
            'last_name': 'Smith',  # Changed last name
            'title': 'Software Developer',
            'bio': 'Test bio',
            'email': 'john@example.com',
            'location': 'New York'
        }
        response = admin_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        profile.refresh_from_db()
        assert profile.last_name == 'Smith'
    
    def test_delete_profile(self, admin_client, profile):
        """Test deleting a profile."""
        url = reverse('profile-detail', kwargs={'pk': profile.pk})
        response = admin_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Profile.objects.count() == 0
