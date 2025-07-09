import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils.text import slugify
from datetime import date

from apps.portfolio.models import Project, ProjectCategory, ProjectImage

@pytest.mark.django_db
class TestProjectCategoryModel:
    """Tests for the ProjectCategory model."""
    
    def test_category_creation(self):
        """Test that a category can be created with required fields."""
        category = ProjectCategory.objects.create(
            name="Test Category"
        )
        assert category.id is not None
        assert category.name == "Test Category"
        assert category.slug == "test-category"  # Auto-generated slug
        
    def test_category_str_representation(self):
        """Test the string representation of the category."""
        category = ProjectCategory.objects.create(name="Test Category")
        assert str(category) == "Test Category"
        
    def test_unique_slug(self):
        """Test that slugs are unique."""
        category1 = ProjectCategory.objects.create(name="Test Category")
        
        # Creating another category with the same name should auto-generate a different slug
        category2 = ProjectCategory.objects.create(name="Test Category")
        assert category1.slug != category2.slug
        
    def test_manual_slug_setting(self):
        """Test that a slug can be manually set."""
        category = ProjectCategory.objects.create(
            name="Test Category",
            slug="custom-slug"
        )
        assert category.slug == "custom-slug"
        
    def test_slug_not_updated_on_name_change(self):
        """Test that slug is not updated when the name changes."""
        category = ProjectCategory.objects.create(name="Test Category")
        original_slug = category.slug
        
        category.name = "Updated Category"
        category.save()
        
        assert category.name == "Updated Category"
        assert category.slug == original_slug


@pytest.mark.django_db
class TestProjectModel:
    """Tests for the Project model."""
    
    @pytest.fixture
    def category(self):
        """Create a test category."""
        return ProjectCategory.objects.create(name="Test Category")
    
    def test_project_creation(self, category):
        """Test that a project can be created with required fields."""
        project = Project.objects.create(
            title="Test Project",
            description="This is a test project description.",
            short_description="Short description",
            thumbnail="projects/thumbnails/test.jpg",
            completion_date=date(2023, 1, 1)
        )
        project.categories.add(category)
        
        assert project.id is not None
        assert project.title == "Test Project"
        assert project.slug == "test-project"
        assert project.categories.count() == 1
        assert project.categories.first() == category
        
    def test_project_str_representation(self):
        """Test the string representation of the project."""
        project = Project.objects.create(
            title="Test Project",
            description="This is a test project description.",
            short_description="Short description",
            thumbnail="projects/thumbnails/test.jpg",
            completion_date=date(2023, 1, 1)
        )
        assert str(project) == "Test Project"
        
    def test_project_ordering(self):
        """Test that projects are ordered by completion date (descending)."""
        project1 = Project.objects.create(
            title="Project 1",
            description="Description 1",
            short_description="Short description 1",
            thumbnail="projects/thumbnails/test1.jpg",
            completion_date=date(2023, 1, 1)
        )
        
        project2 = Project.objects.create(
            title="Project 2",
            description="Description 2",
            short_description="Short description 2",
            thumbnail="projects/thumbnails/test2.jpg",
            completion_date=date(2023, 2, 1)
        )
        
        projects = list(Project.objects.all())
        assert projects[0] == project2  # Most recent project should be first
        assert projects[1] == project1
        
    def test_project_unique_slug(self):
        """Test that project slugs are unique."""
        project1 = Project.objects.create(
            title="Test Project",
            description="Description 1",
            short_description="Short description 1",
            thumbnail="projects/thumbnails/test1.jpg",
            completion_date=date(2023, 1, 1)
        )
        
        project2 = Project.objects.create(
            title="Test Project",
            description="Description 2",
            short_description="Short description 2",
            thumbnail="projects/thumbnails/test2.jpg",
            completion_date=date(2023, 2, 1)
        )
        
        assert project1.slug != project2.slug
        
    def test_project_featured_flag(self):
        """Test the featured flag functionality."""
        project = Project.objects.create(
            title="Test Project",
            description="This is a test project description.",
            short_description="Short description",
            thumbnail="projects/thumbnails/test.jpg",
            completion_date=date(2023, 1, 1),
            featured=True
        )
        
        assert project.featured is True
        
        # Test querying for featured projects
        featured_projects = Project.objects.filter(featured=True)
        assert featured_projects.count() == 1
        assert featured_projects.first() == project


@pytest.mark.django_db
class TestProjectImageModel:
    """Tests for the ProjectImage model."""
    
    @pytest.fixture
    def project(self):
        """Create a test project."""
        return Project.objects.create(
            title="Test Project",
            description="This is a test project description.",
            short_description="Short description",
            thumbnail="projects/thumbnails/test.jpg",
            completion_date=date(2023, 1, 1)
        )
    
    def test_image_creation(self, project):
        """Test that an image can be created for a project."""
        image = ProjectImage.objects.create(
            project=project,
            image="projects/images/test.jpg",
            alt_text="Test image"
        )
        
        assert image.id is not None
        assert image.project == project
        assert image.alt_text == "Test image"
        
    def test_image_str_representation(self, project):
        """Test the string representation of the image."""
        image = ProjectImage.objects.create(
            project=project,
            image="projects/images/test.jpg",
            alt_text="Test image"
        )
        
        assert str(image) == f"Image for {project.title}"
        
    def test_image_ordering(self, project):
        """Test that images are ordered by the order field."""
        image1 = ProjectImage.objects.create(
            project=project,
            image="projects/images/test1.jpg",
            alt_text="Test image 1",
            order=2
        )
        
        image2 = ProjectImage.objects.create(
            project=project,
            image="projects/images/test2.jpg",
            alt_text="Test image 2",
            order=1
        )
        
        images = list(ProjectImage.objects.all())
        assert images[0] == image2  # Lower order should be first
        assert images[1] == image1
        
    def test_project_relation(self, project):
        """Test the relationship between project and images."""
        image1 = ProjectImage.objects.create(
            project=project,
            image="projects/images/test1.jpg",
            alt_text="Test image 1"
        )
        
        image2 = ProjectImage.objects.create(
            project=project,
            image="projects/images/test2.jpg",
            alt_text="Test image 2"
        )
        
        # Test that the project has the correct images
        assert project.images.count() == 2
        assert list(project.images.all()) == [image1, image2]
        
    def test_image_cascade_delete(self, project):
        """Test that images are deleted when the project is deleted."""
        image = ProjectImage.objects.create(
            project=project,
            image="projects/images/test.jpg",
            alt_text="Test image"
        )
        
        # Delete the project
        project.delete()
        
        # Verify the image is also deleted
        assert ProjectImage.objects.count() == 0
