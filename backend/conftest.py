import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """Return an API client for testing."""
    return APIClient()


@pytest.fixture
def authenticated_client(django_user_model):
    """Return an authenticated API client for testing."""
    username = "testuser"
    password = "password"
    user = django_user_model.objects.create_user(username=username, password=password)
    client = APIClient()
    client.force_authenticate(user=user)
    return client
