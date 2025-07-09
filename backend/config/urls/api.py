from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.profile.apis import ProfileViewSet
from apps.resume.apis import EducationViewSet, ExperienceViewSet
from apps.skills.apis import SkillCategoryViewSet, SkillViewSet

router = DefaultRouter()

# Profile URLs
router.register(r'profile', ProfileViewSet, basename='profile')

# Resume URLs
router.register(r'education', EducationViewSet, basename='education')
router.register(r'experience', ExperienceViewSet, basename='experience')

# Skills URLs
router.register(r'skill-categories', SkillCategoryViewSet, basename='skill-category')
router.register(r'skills', SkillViewSet, basename='skill')

urlpatterns = [
    path('', include((router.urls, 'api'))),
]
