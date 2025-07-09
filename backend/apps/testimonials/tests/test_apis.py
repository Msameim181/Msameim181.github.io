import pytest
from django.urls import reverse
from apps.testimonials.models import Testimonial


@pytest.mark.django_db
class TestTestimonialAPI:
    def test_list_testimonials(self, api_client):
        # Create test data
        Testimonial.objects.create(
            name="John Doe",
            position="CEO",
            company="ABC Company",
            content="Great work!",
            rating=5
        )
        Testimonial.objects.create(
            name="Jane Smith",
            position="CTO",
            company="XYZ Tech",
            content="Amazing job!",
            rating=4
        )
        
        # Get API response
        url = reverse('api:testimonial-list')
        response = api_client.get(url)
        
        # Assert response
        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0]['name'] == "John Doe"
        
    def test_retrieve_testimonial(self, api_client):
        # Create test data
        testimonial = Testimonial.objects.create(
            name="John Doe",
            position="CEO",
            company="ABC Company",
            content="Great work!",
            rating=5
        )
        
        # Get API response
        url = reverse('api:testimonial-detail', kwargs={'pk': testimonial.id})
        response = api_client.get(url)
        
        # Assert response
        assert response.status_code == 200
        assert response.data['name'] == "John Doe"
        assert response.data['position'] == "CEO"
        assert response.data['content'] == "Great work!"
        
    def test_filter_featured_testimonials(self, api_client):
        # Create test data
        Testimonial.objects.create(
            name="John Doe",
            position="CEO",
            company="ABC Company",
            content="Great work!",
            rating=5,
            is_featured=True
        )
        Testimonial.objects.create(
            name="Jane Smith",
            position="CTO",
            company="XYZ Tech",
            content="Amazing job!",
            rating=4,
            is_featured=False
        )
        
        # Get API response with filter
        url = reverse('api:testimonial-list') + '?featured=true'
        response = api_client.get(url)
        
        # Assert response
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['name'] == "John Doe"
