import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.portfolio.models import ProjectCategory, Project, ProjectImage


@pytest.mark.django_db
class TestProjectCategoryModel:
    def test_create_category(self):
        category = ProjectCategory.objects.create(
            name="Web Development",
            description="Web development projects",
            order=1
        )
        assert category.name == "Web Development"
        assert category.slug == "web-development"
        assert category.description == "Web development projects"
        assert category.order == 1
    
    def test_str_representation(self):
        category = ProjectCategory.objects.create(name="Web Development")
        assert str(category) == "Web Development"


@pytest.mark.django_db
class TestProjectModel:
    def test_create_project(self):
        category = ProjectCategory.objects.create(name="Web Development")
        project = Project.objects.create(
            title="Portfolio Website",
            category=category,
            description="My personal portfolio website",
            content="Detailed content about the portfolio website",
            technologies="Django, Vue.js",
            start_date="2023-01-01",
            is_featured=True
        )
        
        assert project.title == "Portfolio Website"
        assert project.slug == "portfolio-website"
        assert project.category == category
        assert project.description == "My personal portfolio website"
        assert project.technologies == "Django, Vue.js"
        assert project.is_featured is True
    
    def test_str_representation(self):
        category = ProjectCategory.objects.create(name="Web Development")
        project = Project.objects.create(
            title="Portfolio Website",
            category=category,
            description="My personal portfolio website",
            start_date="2023-01-01"
        )
        assert str(project) == "Portfolio Website"


@pytest.mark.django_db
class TestProjectImageModel:
    def test_create_project_image(self):
        category = ProjectCategory.objects.create(name="Web Development")
        project = Project.objects.create(
            title="Portfolio Website",
            category=category,
            description="My personal portfolio website",
            start_date="2023-01-01"
        )
        
        # Create a test image
        image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',
            content_type='image/jpeg'
        )
        
        image = ProjectImage.objects.create(
            project=project,
            image=image_file,
            caption="Screenshot of the website",
            is_cover=True,
            order=1
        )
        
        assert image.project == project
        assert image.caption == "Screenshot of the website"
        assert image.is_cover is True
        assert image.order == 1
    
    def test_str_representation(self):
        category = ProjectCategory.objects.create(name="Web Development")
        project = Project.objects.create(
            title="Portfolio Website",
            category=category,
            description="My personal portfolio website",
            start_date="2023-01-01"
        )
        
        # Create a test image
        image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',
            content_type='image/jpeg'
        )
        
        image = ProjectImage.objects.create(
            project=project,
            image=image_file
        )
        
        assert str(image) == "Image for Portfolio Website"
