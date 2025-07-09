from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.testimonials.apis import TestimonialViewSet


router = DefaultRouter()

router.register(r'testimonials', TestimonialViewSet, basename='testimonial')

urlpatterns = [
    path('', include((router.urls, 'api'))),
]
