from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.contact.apis import ContactMessageViewSet, ContactInformationViewSet


router = DefaultRouter()

router.register(r'messages', ContactMessageViewSet, basename='contact-message')
router.register(r'information', ContactInformationViewSet, basename='contact-information')

urlpatterns = [
    path('', include((router.urls, 'api'))),
]
