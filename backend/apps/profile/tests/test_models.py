import pytest
from django.core.exceptions import ValidationError
from apps.profile.models import Profile


@pytest.mark.django_db
class TestProfileModel:
    """
    Tests for the Profile model.
    """
    def test_profile_creation(self):
        """Test that a profile can be created with required fields."""
        profile = Profile.objects.create(
            first_name="John",
            last_name="Doe",
            title="Software Developer",
            bio="Test bio",
            email="john@example.com",
            location="New York"
        )
        assert profile.id is not None
        assert profile.first_name == "John"
        assert profile.last_name == "Doe"
        assert profile.title == "Software Developer"
        assert str(profile) == "John Doe"
        assert profile.full_name == "John Doe"
    
    def test_profile_required_fields(self):
        """Test validation for required fields."""
        with pytest.raises(ValidationError):
            profile = Profile(
                first_name="John",
                # last_name is missing
                title="Software Developer",
                bio="Test bio",
                email="john@example.com",
                location="New York"
            )
            profile.full_clean()
    
    def test_profile_email_validation(self):
        """Test email field validation."""
        with pytest.raises(ValidationError):
            profile = Profile(
                first_name="John",
                last_name="Doe",
                title="Software Developer",
                bio="Test bio",
                email="invalid-email",  # Invalid email
                location="New York"
            )
            profile.full_clean()
