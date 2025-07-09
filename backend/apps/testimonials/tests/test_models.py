import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.testimonials.models import Testimonial


@pytest.mark.django_db
class TestTestimonialModel:
    def test_create_testimonial(self):
        testimonial = Testimonial.objects.create(
            name="John Doe",
            position="CEO",
            company="ABC Company",
            content="Great work!",
            rating=5,
            is_featured=True,
            order=1
        )
        
        assert testimonial.name == "John Doe"
        assert testimonial.position == "CEO"
        assert testimonial.company == "ABC Company"
        assert testimonial.content == "Great work!"
        assert testimonial.rating == 5
        assert testimonial.is_featured is True
        assert testimonial.order == 1
    
    def test_str_representation(self):
        testimonial = Testimonial.objects.create(
            name="John Doe",
            position="CEO",
            content="Great work!"
        )
        assert str(testimonial) == "Testimonial from John Doe"
        
    def test_testimonial_with_avatar(self):
        # Create a test image
        avatar_file = SimpleUploadedFile(
            name='test_avatar.jpg',
            content=b'',
            content_type='image/jpeg'
        )
        
        testimonial = Testimonial.objects.create(
            name="John Doe",
            position="CEO",
            content="Great work!",
            avatar=avatar_file
        )
        
        assert testimonial.avatar is not None
        
    def test_testimonial_ordering(self):
        # Create testimonials with different order values
        testimonial1 = Testimonial.objects.create(
            name="John Doe",
            position="CEO",
            content="Great work!",
            order=2
        )
        testimonial2 = Testimonial.objects.create(
            name="Jane Smith",
            position="CTO",
            content="Amazing job!",
            order=1
        )
        
        testimonials = Testimonial.objects.all()
        # First one should be Jane Smith with order=1
        assert testimonials[0] == testimonial2
        # Second one should be John Doe with order=2
        assert testimonials[1] == testimonial1
