from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.portfolio.apis import ProjectCategoryViewSet, ProjectViewSet


router = DefaultRouter()

router.register(r'project-categories', ProjectCategoryViewSet, basename='project-category')
router.register(r'projects', ProjectViewSet, basename='project')

urlpatterns = [
    path('', include((router.urls, 'api'))),
]
