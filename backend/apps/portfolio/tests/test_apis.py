import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.portfolio.models import ProjectCategory, Project


@pytest.mark.django_db
class TestProjectCategoryAPI:
    def test_list_categories(self, api_client):
        # Create test data
        ProjectCategory.objects.create(name="Web Development", order=1)
        ProjectCategory.objects.create(name="Mobile Development", order=2)
        
        # Get API response
        url = reverse('api:project-category-list')
        response = api_client.get(url)
        
        # Assert response
        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0]['name'] == "Web Development"
        
    def test_retrieve_category(self, api_client):
        # Create test data
        category = ProjectCategory.objects.create(
            name="Web Development", 
            slug="web-development",
            description="Web development projects"
        )
        
        # Get API response
        url = reverse('api:project-category-detail', kwargs={'slug': category.slug})
        response = api_client.get(url)
        
        # Assert response
        assert response.status_code == 200
        assert response.data['name'] == "Web Development"
        assert response.data['description'] == "Web development projects"


@pytest.mark.django_db
class TestProjectAPI:
    def test_list_projects(self, api_client):
        # Create test data
        category = ProjectCategory.objects.create(name="Web Development")
        Project.objects.create(
            title="Portfolio Website",
            slug="portfolio-website",
            category=category,
            description="My personal portfolio website",
            start_date="2023-01-01"
        )
        
        # Get API response
        url = reverse('api:project-list')
        response = api_client.get(url)
        
        # Assert response
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['title'] == "Portfolio Website"
        
    def test_retrieve_project(self, api_client):
        # Create test data
        category = ProjectCategory.objects.create(name="Web Development")
        project = Project.objects.create(
            title="Portfolio Website",
            slug="portfolio-website",
            category=category,
            description="My personal portfolio website",
            content="Detailed content about the portfolio website",
            technologies="Django, Vue.js",
            start_date="2023-01-01"
        )
        
        # Get API response
        url = reverse('api:project-detail', kwargs={'slug': project.slug})
        response = api_client.get(url)
        
        # Assert response
        assert response.status_code == 200
        assert response.data['title'] == "Portfolio Website"
        assert response.data['technologies'] == "Django, Vue.js"
        assert response.data['content'] == "Detailed content about the portfolio website"
        
    def test_filter_projects_by_category(self, api_client):
        # Create test data
        web_category = ProjectCategory.objects.create(name="Web Development", slug="web")
        mobile_category = ProjectCategory.objects.create(name="Mobile Development", slug="mobile")
        
        Project.objects.create(
            title="Portfolio Website",
            slug="portfolio-website",
            category=web_category,
            description="My personal portfolio website",
            start_date="2023-01-01"
        )
        Project.objects.create(
            title="Mobile App",
            slug="mobile-app",
            category=mobile_category,
            description="A mobile app",
            start_date="2023-02-01"
        )
        
        # Get API response with filter
        url = reverse('api:project-list') + '?category=web'
        response = api_client.get(url)
        
        # Assert response
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['title'] == "Portfolio Website"
