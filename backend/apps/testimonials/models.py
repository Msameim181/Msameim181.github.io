from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    avatar_thumbnail = ImageSpecField(
        source='avatar',
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={'quality': 85}
    )
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(
        choices=[(i, f"{i} stars") for i in range(1, 6)],
        default=5
    )
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"Testimonial from {self.name}"
