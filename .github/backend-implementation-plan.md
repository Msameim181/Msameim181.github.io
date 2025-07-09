# Backend Implementation Plan

This document outlines the detailed implementation plan for converting the static portfolio website to a dynamic Django application with Vue.js frontend. It includes specific tasks, testing procedures, and progress tracking.

## Phase 1: Project Setup & Configuration

### 1.1 Create Django Project Structure

**Tasks:**
- Set up Django project following HackSoftware Django Styleguide
- Create directory structure for apps, settings, and templates
- Configure virtual environment

**Implementation:**
```bash
# Create project directory
mkdir -p portfolio_backend
cd portfolio_backend

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install Django and initial packages
pip install django djangorestframework django-cors-headers pytest pytest-django

# Create Django project with settings module
django-admin startproject config .
mkdir -p config/settings
```

**Expected Directory Structure:**
```
portfolio_backend/
├── config/
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── __init__.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── apps/
│   ├── __init__.py
├── templates/
├── static/
├── media/
├── manage.py
├── pytest.ini
└── requirements.txt
```

**Tests:**
- `test_project_structure.py`: Verify the directory structure matches the expected layout
- `test_settings_module.py`: Verify settings configuration works correctly

### 1.2 Configure Settings

**Tasks:**
- Split settings into base, local, and production
- Configure database settings
- Set up static and media files settings
- Configure security settings

**Implementation (config/settings/base.py):**
```python
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'corsheaders',
    
    # Local apps will be added here
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = False
```

**Tests:**
- `test_settings_imports.py`: Verify settings import correctly
- `test_environment_settings.py`: Verify environment-specific settings load correctly

### 1.3 Docker Configuration

**Tasks:**
- Create Dockerfile for Django application
- Create docker-compose.yml for development environment
- Configure volumes for persistent data

**Implementation (Dockerfile):**
```Dockerfile
FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        postgresql-client \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project
COPY . /app/

# Run entrypoint script
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

# Run server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
```

**Implementation (docker-compose.yml):**
```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - ./.env
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_DB=portfolio

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    env_file:
      - ./.env
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.local

volumes:
  postgres_data:
```

**Tests:**
- `test_docker_build.py`: Verify Docker container builds successfully
- `test_docker_compose.py`: Verify docker-compose works correctly

## Phase 2: Core Models & Database

### 2.1 Profile Model

**Tasks:**
- Create profile app
- Implement Profile model
- Create serializers and API views

**Implementation (apps/profile/models.py):**
```python
from django.db import models
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):
    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last Name"), max_length=100)
    title = models.CharField(_("Professional Title"), max_length=200)
    bio = models.TextField(_("Bio"))
    avatar = models.ImageField(_("Avatar"), upload_to="profile/")
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Phone"), max_length=20, blank=True)
    location = models.CharField(_("Location"), max_length=200)
    
    # Social links
    github = models.URLField(_("GitHub"), blank=True)
    linkedin = models.URLField(_("LinkedIn"), blank=True)
    twitter = models.URLField(_("Twitter"), blank=True)
    website = models.URLField(_("Personal Website"), blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
```

**Implementation (apps/profile/serializers.py):**
```python
from rest_framework import serializers
from apps.profile.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id', 'first_name', 'last_name', 'title', 'bio', 'avatar',
            'email', 'phone', 'location', 'github', 'linkedin',
            'twitter', 'website', 'created_at', 'updated_at'
        ]
```

**Implementation (apps/profile/apis.py):**
```python
from rest_framework import viewsets
from apps.profile.models import Profile
from apps.profile.serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
```

**Tests:**
- `test_profile_model.py`: Test model fields, methods, and constraints
- `test_profile_serializer.py`: Test serializer functionality
- `test_profile_api.py`: Test API endpoints for CRUD operations

### 2.2 Education Model

**Tasks:**
- Create Education model in the resume app
- Implement serializers and API views

**Implementation (apps/resume/models.py):**
```python
from django.db import models
from django.utils.translation import gettext_lazy as _

class Education(models.Model):
    institution = models.CharField(_("Institution"), max_length=200)
    degree = models.CharField(_("Degree"), max_length=200)
    field_of_study = models.CharField(_("Field of Study"), max_length=200)
    start_date = models.DateField(_("Start Date"))
    end_date = models.DateField(_("End Date"), null=True, blank=True)
    description = models.TextField(_("Description"), blank=True)
    location = models.CharField(_("Location"), max_length=200)
    is_current = models.BooleanField(_("Current"), default=False)
    order = models.PositiveIntegerField(_("Order"), default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Education")
        verbose_name_plural = _("Education")
        ordering = ['order', '-start_date']
    
    def __str__(self):
        return f"{self.degree} at {self.institution}"
```

**Tests:**
- `test_education_model.py`: Test model fields, methods, and constraints
- `test_education_serializer.py`: Test serializer functionality
- `test_education_api.py`: Test API endpoints for CRUD operations

### 2.3 Experience Model

**Tasks:**
- Create Experience model in the resume app
- Implement serializers and API views

**Implementation (apps/resume/models.py):**
```python
class Experience(models.Model):
    company = models.CharField(_("Company"), max_length=200)
    position = models.CharField(_("Position"), max_length=200)
    start_date = models.DateField(_("Start Date"))
    end_date = models.DateField(_("End Date"), null=True, blank=True)
    description = models.TextField(_("Description"))
    location = models.CharField(_("Location"), max_length=200)
    is_current = models.BooleanField(_("Current"), default=False)
    order = models.PositiveIntegerField(_("Order"), default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Experience")
        verbose_name_plural = _("Experience")
        ordering = ['order', '-start_date']
    
    def __str__(self):
        return f"{self.position} at {self.company}"
```

**Tests:**
- `test_experience_model.py`: Test model fields, methods, and constraints
- `test_experience_serializer.py`: Test serializer functionality
- `test_experience_api.py`: Test API endpoints for CRUD operations

### 2.4 Skills Model

**Tasks:**
- Create Skills app and models
- Implement serializers and API views

**Implementation (apps/skills/models.py):**
```python
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class SkillCategory(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    order = models.PositiveIntegerField(_("Order"), default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Skill Category")
        verbose_name_plural = _("Skill Categories")
        ordering = ['order']
    
    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    category = models.ForeignKey(
        SkillCategory, 
        on_delete=models.CASCADE,
        related_name="skills"
    )
    proficiency = models.PositiveSmallIntegerField(
        _("Proficiency"),
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    icon = models.FileField(_("Icon"), upload_to="skills/", blank=True)
    order = models.PositiveIntegerField(_("Order"), default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")
        ordering = ['category', 'order']
    
    def __str__(self):
        return self.name
```

**Tests:**
- `test_skill_category_model.py`: Test model fields and methods
- `test_skill_model.py`: Test model fields, methods, and constraints
- `test_skills_serializer.py`: Test serializer functionality
- `test_skills_api.py`: Test API endpoints for CRUD operations

### 2.5 Project Model

**Tasks:**
- Create Portfolio app and models
- Implement serializers and API views

**Implementation (apps/portfolio/models.py):**
```python
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

class ProjectCategory(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Project Category")
        verbose_name_plural = _("Project Categories")
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Project(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(_("Slug"), unique=True)
    description = models.TextField(_("Description"))
    short_description = models.CharField(_("Short Description"), max_length=255)
    thumbnail = models.ImageField(_("Thumbnail"), upload_to="projects/thumbnails/")
    categories = models.ManyToManyField(
        ProjectCategory,
        related_name="projects"
    )
    client = models.CharField(_("Client"), max_length=200, blank=True)
    completion_date = models.DateField(_("Completion Date"))
    project_url = models.URLField(_("Project URL"), blank=True)
    github_url = models.URLField(_("GitHub URL"), blank=True)
    featured = models.BooleanField(_("Featured"), default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ['-completion_date']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(_("Image"), upload_to="projects/images/")
    alt_text = models.CharField(_("Alt Text"), max_length=200)
    order = models.PositiveIntegerField(_("Order"), default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Project Image")
        verbose_name_plural = _("Project Images")
        ordering = ['order']
    
    def __str__(self):
        return f"Image for {self.project.title}"
```

**Tests:**
- `test_project_category_model.py`: Test model fields and methods
- `test_project_model.py`: Test model fields, methods, and constraints
- `test_project_image_model.py`: Test model fields and constraints
- `test_portfolio_serializers.py`: Test serializer functionality
- `test_portfolio_api.py`: Test API endpoints for CRUD operations

### 2.6 Testimonial Model

**Tasks:**
- Create Testimonial model
- Implement serializers and API views

**Implementation (apps/testimonials/models.py):**
```python
from django.db import models
from django.utils.translation import gettext_lazy as _

class Testimonial(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    position = models.CharField(_("Position"), max_length=200)
    company = models.CharField(_("Company"), max_length=200, blank=True)
    content = models.TextField(_("Content"))
    avatar = models.ImageField(_("Avatar"), upload_to="testimonials/", blank=True)
    rating = models.PositiveSmallIntegerField(_("Rating"), default=5)
    active = models.BooleanField(_("Active"), default=True)
    order = models.PositiveIntegerField(_("Order"), default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Testimonial")
        verbose_name_plural = _("Testimonials")
        ordering = ['order']
    
    def __str__(self):
        return f"Testimonial from {self.name}"
```

**Tests:**
- `test_testimonial_model.py`: Test model fields and methods
- `test_testimonial_serializer.py`: Test serializer functionality
- `test_testimonial_api.py`: Test API endpoints for CRUD operations

### 2.7 BlogPost Model

**Tasks:**
- Create Blog app and models
- Implement serializers and API views

**Implementation (apps/blog/models.py):**
```python
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()

class BlogCategory(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Blog Category")
        verbose_name_plural = _("Blog Categories")
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class BlogPost(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(_("Slug"), unique=True)
    content = models.TextField(_("Content"))
    excerpt = models.TextField(_("Excerpt"), blank=True)
    featured_image = models.ImageField(_("Featured Image"), upload_to="blog/")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blog_posts"
    )
    categories = models.ManyToManyField(
        BlogCategory,
        related_name="blog_posts"
    )
    published_date = models.DateTimeField(_("Published Date"), null=True, blank=True)
    is_published = models.BooleanField(_("Published"), default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Blog Post")
        verbose_name_plural = _("Blog Posts")
        ordering = ['-published_date', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    name = models.CharField(_("Name"), max_length=100)
    email = models.EmailField(_("Email"))
    content = models.TextField(_("Content"))
    approved = models.BooleanField(_("Approved"), default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"
```

**Tests:**
- `test_blog_category_model.py`: Test model fields and methods
- `test_blog_post_model.py`: Test model fields, methods, and constraints
- `test_comment_model.py`: Test model fields and constraints
- `test_blog_serializers.py`: Test serializer functionality
- `test_blog_api.py`: Test API endpoints for CRUD operations

### 2.8 Contact Model

**Tasks:**
- Create Contact app and models
- Implement serializers and API views
- Migrate existing FastAPI contact form to Django

**Implementation (apps/contact/models.py):**
```python
from django.db import models
from django.utils.translation import gettext_lazy as _

class Contact(models.Model):
    STATUS_CHOICES = (
        ('new', _('New')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
        ('spam', _('Spam')),
    )
    
    name = models.CharField(_("Name"), max_length=100)
    email = models.EmailField(_("Email"))
    subject = models.CharField(_("Subject"), max_length=200)
    message = models.TextField(_("Message"))
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    ip_address = models.GenericIPAddressField(_("IP Address"), blank=True, null=True)
    user_agent = models.TextField(_("User Agent"), blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Contact from {self.name} - {self.subject}"
```

**Tests:**
- `test_contact_model.py`: Test model fields and methods
- `test_contact_serializer.py`: Test serializer functionality
- `test_contact_api.py`: Test API endpoints for CRUD operations
- `test_contact_form_submission.py`: Test form submission and validation

## Phase 3: Admin Interface

### 3.1 Configure Admin Interface

**Tasks:**
- Configure Django admin for all models
- Customize admin views
- Add filtering and search

**Implementation (apps/profile/admin.py):**
```python
from django.contrib import admin
from apps.profile.models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'title', 'email')
    search_fields = ('first_name', 'last_name', 'title', 'bio')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'title', 'bio', 'avatar')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'location')
        }),
        ('Social Links', {
            'fields': ('github', 'linkedin', 'twitter', 'website')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
```

**Tests:**
- `test_admin_login.py`: Test admin login functionality
- `test_admin_models.py`: Test admin model registration and configuration

### 3.2 Implement CKEditor

**Tasks:**
- Install django-ckeditor
- Configure CKEditor for rich text fields
- Customize CKEditor settings

**Implementation:**
```python
# settings/base.py
INSTALLED_APPS += [
    'ckeditor',
    'ckeditor_uploader',
]

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'height': 300,
        'width': '100%',
    },
}

# Model implementation
from ckeditor_uploader.fields import RichTextUploadingField

class BlogPost(models.Model):
    # ...
    content = RichTextUploadingField(_("Content"))
    # ...
```

**Tests:**
- `test_ckeditor_fields.py`: Test CKEditor field rendering and functionality

### 3.3 Image Upload and Optimization

**Tasks:**
- Install and configure django-imagekit
- Implement image resizing and optimization
- Create thumbnail generation functions

**Implementation:**
```python
# settings/base.py
INSTALLED_APPS += [
    'imagekit',
]

# Model implementation
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class Project(models.Model):
    # ...
    thumbnail = ProcessedImageField(
        upload_to='projects/thumbnails/',
        processors=[ResizeToFill(800, 600)],
        format='JPEG',
        options={'quality': 85},
        verbose_name=_("Thumbnail")
    )
    # ...
```

**Tests:**
- `test_image_upload.py`: Test image upload functionality
- `test_image_optimization.py`: Test image processing and optimization

## Phase 4: API Development

### 4.1 RESTful API Endpoints

**Tasks:**
- Configure Django REST Framework
- Implement viewsets for all models
- Set up URL routing

**Implementation (config/urls.py):**
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from apps.profile.apis import ProfileViewSet
from apps.resume.apis import EducationViewSet, ExperienceViewSet
from apps.skills.apis import SkillCategoryViewSet, SkillViewSet
from apps.portfolio.apis import ProjectCategoryViewSet, ProjectViewSet
from apps.testimonials.apis import TestimonialViewSet
from apps.blog.apis import BlogCategoryViewSet, BlogPostViewSet, CommentViewSet
from apps.contact.apis import ContactViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'education', EducationViewSet)
router.register(r'experience', ExperienceViewSet)
router.register(r'skill-categories', SkillCategoryViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'project-categories', ProjectCategoryViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'testimonials', TestimonialViewSet)
router.register(r'blog-categories', BlogCategoryViewSet)
router.register(r'blog-posts', BlogPostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'contacts', ContactViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**Tests:**
- `test_api_endpoints.py`: Test all API endpoints for proper responses
- `test_api_authentication.py`: Test authentication and permissions

### 4.2 Authentication and Permissions

**Tasks:**
- Set up JWT authentication
- Configure permissions for different endpoints
- Implement custom permission classes

**Implementation:**
```python
# settings/base.py
INSTALLED_APPS += [
    'rest_framework_simplejwt',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}

# Custom permissions
from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
```

**Tests:**
- `test_api_authentication.py`: Test authentication methods
- `test_api_permissions.py`: Test permission classes

### 4.3 Filtering, Pagination, and Search

**Tasks:**
- Configure filtering with django-filter
- Set up search functionality
- Implement pagination

**Implementation:**
```python
# settings/base.py
INSTALLED_APPS += [
    'django_filters',
]

REST_FRAMEWORK = {
    # ... other settings
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# API ViewSet
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['categories', 'featured']
    search_fields = ['title', 'description', 'client']
    ordering_fields = ['completion_date', 'created_at']
```

**Tests:**
- `test_api_filtering.py`: Test filtering functionality
- `test_api_pagination.py`: Test pagination functionality
- `test_api_search.py`: Test search functionality

## Phase 5: Contact Form Migration

### 5.1 Migrate FastAPI Contact Form

**Tasks:**
- Create Django view for contact form
- Implement form validation
- Migrate existing data from SQLite database

**Implementation (apps/contact/views.py):**
```python
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.contact.models import Contact
from apps.contact.serializers import ContactSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def contact_form_view(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        # Add IP address and user agent
        serializer.validated_data['ip_address'] = request.META.get('REMOTE_ADDR')
        serializer.validated_data['user_agent'] = request.META.get('HTTP_USER_AGENT', '')
        
        contact = serializer.save()
        
        # Send email notification
        send_contact_notification(contact)
        
        return Response(
            {"success": True, "message": "Message sent successfully!"}, 
            status=status.HTTP_201_CREATED
        )
    return Response(
        {"success": False, "errors": serializer.errors}, 
        status=status.HTTP_400_BAD_REQUEST
    )
```

**Tests:**
- `test_contact_form_view.py`: Test contact form view functionality
- `test_contact_form_validation.py`: Test form validation

### 5.2 Email Notification System

**Tasks:**
- Configure Django email settings
- Implement email notification for new contact submissions
- Create email templates

**Implementation (apps/contact/utils.py):**
```python
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def send_contact_notification(contact):
    subject = f"New Contact Form Submission: {contact.subject}"
    html_message = render_to_string(
        'contact/email_notification.html',
        {'contact': contact}
    )
    
    send_mail(
        subject=subject,
        message=f"New message from {contact.name} ({contact.email}): {contact.message}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],
        html_message=html_message,
        fail_silently=False,
    )
```

**Tests:**
- `test_email_notification.py`: Test email sending functionality
- `test_email_templates.py`: Test email templates rendering

### 5.3 Anti-spam Measures

**Tasks:**
- Implement CAPTCHA protection
- Add honeypot field
- Configure rate limiting

**Implementation:**
```python
# settings/base.py
INSTALLED_APPS += [
    'django_recaptcha',
]

RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')

# Contact Form
from django_recaptcha.fields import ReCaptchaField

class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField()
    honeypot = forms.CharField(
        required=False,
        label="Leave empty",
        widget=forms.TextInput(attrs={'style': 'display:none;'})
    )
    
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
    
    def clean(self):
        cleaned_data = super().clean()
        honeypot = cleaned_data.get('honeypot')
        if honeypot:
            raise forms.ValidationError(
                "Spam protection triggered. Please try again."
            )
        return cleaned_data
```

**Tests:**
- `test_captcha_validation.py`: Test CAPTCHA functionality
- `test_honeypot_validation.py`: Test honeypot field
- `test_rate_limiting.py`: Test rate limiting functionality

## Phase 6: Data Migration

### 6.1 Create Data Migration Scripts

**Tasks:**
- Create migration scripts to import data from static HTML
- Parse and import existing data

**Implementation (apps/portfolio/management/commands/import_projects.py):**
```python
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import os
from django.conf import settings
from apps.portfolio.models import Project, ProjectCategory
from django.utils.text import slugify
from django.core.files import File
import datetime

class Command(BaseCommand):
    help = 'Import projects from static HTML'
    
    def handle(self, *args, **options):
        html_path = os.path.join(settings.BASE_DIR, '..', 'portfolio.html')
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        # Find all project elements
        project_elements = soup.select('.portfolio-item')
        
        for element in project_elements:
            title_elem = element.select_one('.portfolio-info h3')
            if not title_elem:
                continue
                
            title = title_elem.text.strip()
            
            # Get or create project
            project, created = Project.objects.get_or_create(
                title=title,
                defaults={
                    'slug': slugify(title),
                    'short_description': element.select_one('.portfolio-info p').text.strip() if element.select_one('.portfolio-info p') else '',
                    'completion_date': datetime.date.today(),  # Default to today
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created project: {project.title}'))
            else:
                self.stdout.write(f'Project already exists: {project.title}')
                
            # Add categories
            category_names = [cat.text.strip() for cat in element.select('.portfolio-category')]
            for cat_name in category_names:
                category, _ = ProjectCategory.objects.get_or_create(name=cat_name)
                project.categories.add(category)
```

**Tests:**
- `test_data_migration_scripts.py`: Test data import functionality
- `test_html_parsing.py`: Test HTML parsing functionality

### 6.2 Implement Fixtures

**Tasks:**
- Create fixture files for initial data
- Implement commands to load fixtures

**Implementation:**
```json
// fixtures/initial_data.json
[
  {
    "model": "profile.profile",
    "pk": 1,
    "fields": {
      "first_name": "Mohammad Mahdi",
      "last_name": "Samei",
      "title": "ML & AI Developer",
      "bio": "Detail-oriented ML & AI Developer with experience in developing and deploying machine learning models...",
      "email": "contact@example.com",
      "location": "Tehran, Iran",
      "github": "https://github.com/Msameim181",
      "linkedin": "https://linkedin.com/in/msameim181"
    }
  }
]
```

**Tests:**
- `test_fixtures_loading.py`: Test fixture loading functionality

## Phase 7: Testing & Documentation

### 7.1 Comprehensive Test Suite

**Tasks:**
- Configure pytest for Django
- Create comprehensive test suite
- Set up test coverage reporting

**Implementation (pytest.ini):**
```ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings.test
python_files = test_*.py
testpaths = apps
```

**Implementation (conftest.py):**
```python
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='password123'
    )
    return user

@pytest.fixture
def admin_client(admin_user, api_client):
    api_client.force_authenticate(user=admin_user)
    return api_client
```

**Tests:**
- `test_test_suite.py`: Meta test to verify test suite functionality
- `test_coverage.py`: Test coverage reporting

### 7.2 API Documentation

**Tasks:**
- Install and configure drf-spectacular
- Generate API schema
- Create API documentation

**Implementation:**
```python
# settings/base.py
INSTALLED_APPS += [
    'drf_spectacular',
]

REST_FRAMEWORK = {
    # ... other settings
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Portfolio API',
    'DESCRIPTION': 'API for dynamic portfolio website',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# urls.py
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```

**Tests:**
- `test_api_documentation.py`: Test API schema generation
- `test_api_docs_views.py`: Test documentation views

## Phase 8: Integration & Deployment

### 8.1 Vue.js and Django Integration

**Tasks:**
- Configure Django for serving Vue.js
- Set up CORS for API access
- Implement API service in Vue.js

**Implementation (settings/base.py):**
```python
MIDDLEWARE = [
    # ... other middleware
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # ... other middleware
]

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://localhost:3000",
]

CORS_ALLOW_CREDENTIALS = True
```

**Tests:**
- `test_cors_settings.py`: Test CORS configuration
- `test_vue_integration.py`: Test Vue.js API access

### 8.2 Production Configuration

**Tasks:**
- Configure Django settings for production
- Set up Gunicorn and Nginx
- Configure SSL

**Implementation (settings/production.py):**
```python
from .base import *

DEBUG = False
ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOST', 'example.com')]

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
```

**Tests:**
- `test_production_settings.py`: Test production settings
- `test_security_settings.py`: Test security configurations

### 8.3 Deployment Script

**Tasks:**
- Create deployment script
- Configure Docker for production
- Set up database backup system

**Implementation (docker-compose.prod.yml):**
```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - ./.env.prod
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_DB=${DB_NAME}
    restart: always
    
  web:
    build:
      context: .
      dockerfile: Dockerfile.prod
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    env_file:
      - ./.env.prod
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.production
    depends_on:
      - db
    restart: always
    
  nginx:
    image: nginx:1.19
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/usr/share/nginx/html/static
      - media_volume:/usr/share/nginx/html/media
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    depends_on:
      - web
    restart: always
      
  certbot:
    image: certbot/certbot
    volumes:
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

**Tests:**
- `test_docker_production.py`: Test Docker production configuration
- `test_nginx_configuration.py`: Test Nginx configuration

## Test Suite Example Implementation

Here are example implementations for some of the key test files:

**test_profile_model.py:**
```python
import pytest
from django.core.exceptions import ValidationError
from apps.profile.models import Profile

@pytest.mark.django_db
class TestProfileModel:
    def test_profile_creation(self):
        profile = Profile.objects.create(
            first_name="John",
            last_name="Doe",
            title="Software Developer",
            bio="Test bio",
            email="john@example.com",
            location="New York"
        )
        assert profile.id is not None
        assert str(profile) == "John Doe"
        
    def test_profile_email_validation(self):
        with pytest.raises(ValidationError):
            profile = Profile(
                first_name="John",
                last_name="Doe",
                title="Software Developer",
                bio="Test bio",
                email="invalid-email",
                location="New York"
            )
            profile.full_clean()
```

**test_profile_api.py:**
```python
import pytest
from django.urls import reverse
from rest_framework import status
from apps.profile.models import Profile

@pytest.mark.django_db
class TestProfileAPI:
    def test_list_profiles(self, api_client):
        url = reverse('profile-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        
    def test_create_profile_unauthorized(self, api_client):
        url = reverse('profile-list')
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "title": "Software Developer",
            "bio": "Test bio",
            "email": "john@example.com",
            "location": "New York"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_create_profile_authorized(self, admin_client):
        url = reverse('profile-list')
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "title": "Software Developer",
            "bio": "Test bio",
            "email": "john@example.com",
            "location": "New York"
        }
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Profile.objects.count() == 1
```

**test_contact_form_submission.py:**
```python
import pytest
from django.urls import reverse
from rest_framework import status
from apps.contact.models import Contact

@pytest.mark.django_db
class TestContactFormSubmission:
    def test_contact_form_valid_submission(self, api_client):
        url = reverse('contact-form')
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "subject": "Test Subject",
            "message": "This is a test message."
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["success"] is True
        assert Contact.objects.count() == 1
        
    def test_contact_form_invalid_email(self, api_client):
        url = reverse('contact-form')
        data = {
            "name": "John Doe",
            "email": "invalid-email",
            "subject": "Test Subject",
            "message": "This is a test message."
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False
        assert "email" in response.data["errors"]
        assert Contact.objects.count() == 0
```
