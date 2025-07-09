# Django Project Structure for Dynamic Portfolio

This file contains the recommended Django project structure for converting the static portfolio website into a dynamic one following the [HackSoftware Django-Styleguide](https://github.com/HackSoftware/Django-Styleguide).

## Initial Setup

```bash
# Create a new Django project
django-admin startproject config .

# Create a directory for apps
mkdir -p apps

# Create necessary apps
django-admin startapp accounts apps/accounts
django-admin startapp core apps/core
django-admin startapp profile apps/profile
django-admin startapp portfolio apps/portfolio
django-admin startapp blog apps/blog
django-admin startapp contact apps/contact

# Create directories for templates and static files
mkdir -p templates/includes
mkdir -p static/{css,js,images}
mkdir -p media/{profile,projects,blog,testimonials,clients}
```

## Project Structure

```
.
├── apps/
│   ├── __init__.py
│   ├── accounts/            # User authentication app
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── tests/
│   ├── core/                # Core functionality
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── tests/
│   ├── profile/             # Personal profile management
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── tests/
│   ├── portfolio/           # Portfolio projects management
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── tests/
│   ├── blog/                # Blog posts management
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── tests/
│   └── contact/             # Contact form processing
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── serializers.py
│       ├── services.py
│       ├── urls.py
│       ├── views.py
│       └── tests/
├── config/                  # Django project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py          # Base settings
│   │   ├── local.py         # Development settings
│   │   └── production.py    # Production settings
│   ├── urls.py
│   ├── api_urls.py          # API endpoints
│   └── wsgi.py
├── templates/               # Django templates
│   ├── base.html            # Base template
│   ├── index.html           # Home page
│   ├── resume.html          # Resume page
│   ├── portfolio.html       # Portfolio page
│   ├── single-project.html  # Project detail page
│   ├── blog.html            # Blog listing page
│   ├── single-post.html     # Blog post detail page
│   ├── contact.html         # Contact page
│   └── includes/            # Reusable template fragments
│       ├── meta.html        # Meta tags
│       ├── navigation.html  # Main navigation
│       └── sidebar.html     # Sidebar with profile info
├── static/                  # Static assets
│   ├── css/
│   ├── js/
│   └── images/
├── media/                   # User uploaded files
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore file
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile               # Docker configuration
├── manage.py                # Django management script
└── requirements.txt         # Python dependencies
```

## Key Models

### Profile Models (apps/profile/models.py)

```python
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='profile/')
    position = models.CharField(max_length=100)
    bio = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    birthday = models.DateField()
    location = models.CharField(max_length=100)
    resume_file = models.FileField(upload_to='profile/files/')
    
    def __str__(self):
        return self.name

class SocialLink(models.Model):
    PLATFORM_CHOICES = (
        ('linkedin', 'LinkedIn'),
        ('github', 'GitHub'),
        ('telegram', 'Telegram'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
    )
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    url = models.URLField()
    icon = models.CharField(max_length=50)  # CSS class for icon
    
    def __str__(self):
        return f"{self.profile.name} - {self.get_platform_display()}"

class Badge(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='badges')
    text = models.CharField(max_length=100)
    
    def __str__(self):
        return self.text

class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', '-end_date']
        verbose_name_plural = 'Education'
    
    def __str__(self):
        return f"{self.degree} at {self.institution}"

class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experience')
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', '-end_date']
    
    def __str__(self):
        return f"{self.position} at {self.company}"

class Skill(models.Model):
    CATEGORY_CHOICES = (
        ('technical', 'Technical Skills'),
        ('language', 'Languages'),
        ('other', 'Other Skills'),
    )
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    experience = models.CharField(max_length=100, blank=True)
    proficiency = models.IntegerField(default=0)  # 0-100
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['category', 'order']
    
    def __str__(self):
        return self.name
```

### Portfolio Models (apps/portfolio/models.py)

```python
from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='projects')
    thumbnail = models.ImageField(upload_to='projects/')
    client = models.CharField(max_length=100, blank=True)
    date = models.DateField()
    description = models.TextField()
    project_url = models.URLField(blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Image for {self.project.title}"
```

### Blog Models (apps/blog/models.py)

```python
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()

class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = 'Blog Categories'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name='posts')
    featured_image = models.ImageField(upload_to='blog/')
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    avatar = models.ImageField(upload_to='blog/comments/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"
```

### Testimonials and Clients Models (apps/core/models.py)

```python
from django.db import models

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='testimonials/')
    position = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    date = models.DateField()
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Testimonial from {self.name}"

class Client(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='clients/')
    url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name
```

### Contact Models (apps/contact/models.py)

```python
from django.db import models

class ContactRequest(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Contact from {self.full_name} ({self.created_at.strftime('%Y-%m-%d')})"
```

## Settings Configuration

### Base Settings (config/settings/base.py)

```python
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-key-for-development')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'corsheaders',
    'ckeditor',
    
    # Project apps
    'apps.accounts',
    'apps.core',
    'apps.profile',
    'apps.portfolio',
    'apps.blog',
    'apps.contact',
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
        'DIRS': [BASE_DIR / 'templates'],
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
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
]

# CKEditor settings
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
}
```

### Local Settings (config/settings/local.py)

```python
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Add Django Debug Toolbar
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']

# Disable CORS in development
CORS_ALLOW_ALL_ORIGINS = True
```

### Production Settings (config/settings/production.py)

```python
from .base import *

DEBUG = False

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS', '*').split(',')]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'portfolio'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Security settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

# CORS settings
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
```

## URL Configuration

### Main URLs (config/urls.py)

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('portfolio/', include('apps.portfolio.urls')),
    path('blog/', include('apps.blog.urls')),
    path('contact/', include('apps.contact.urls')),
    path('api/', include('config.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
```

### API URLs (config/api_urls.py)

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.profile.views import ProfileViewSet
from apps.portfolio.views import CategoryViewSet, ProjectViewSet
from apps.blog.views import BlogCategoryViewSet, BlogPostViewSet, CommentViewSet
from apps.core.views import TestimonialViewSet, ClientViewSet
from apps.contact.views import ContactViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'blog/categories', BlogCategoryViewSet)
router.register(r'blog/posts', BlogPostViewSet)
router.register(r'blog/comments', CommentViewSet)
router.register(r'testimonials', TestimonialViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'contact', ContactViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]
```

## Docker Configuration

### Dockerfile

```dockerfile
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "config.wsgi:application"]
```

### Docker Compose

```yaml
version: '3.7'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    restart: always
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    env_file:
      - .env
    depends_on:
      - db
    networks:
      - portfolio_network

  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - .env
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_DB=${DB_NAME}
    networks:
      - portfolio_network

  nginx:
    image: nginx:latest
    ports:
      - "6549:80"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - static_volume:/var/html/static
      - media_volume:/var/html/media
    depends_on:
      - web
    networks:
      - portfolio_network

networks:
  portfolio_network:

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

## Requirements File

```
# Django and extensions
Django==4.2.7
django-cors-headers==4.3.1
django-ckeditor==6.7.0
django-filter==23.3
django-debug-toolbar==4.2.0

# REST API
djangorestframework==3.14.0

# Database
psycopg2-binary==2.9.9

# Image processing
Pillow==10.1.0

# Environment variables
python-dotenv==1.0.0

# Telegram integration
python-telegram-bot==20.6

# Web server
gunicorn==21.2.0

# Development tools
black==23.10.1
flake8==6.1.0
isort==5.12.0
```

## Environment Variables (.env.example)

```
# Django settings
SECRET_KEY=change-this-to-a-secure-random-key
DEBUG=False
ALLOWED_HOSTS=example.com,www.example.com

# Database settings
DB_NAME=portfolio
DB_USER=postgres
DB_PASSWORD=secure_password_here
DB_HOST=db
DB_PORT=5432

# Email settings
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=your-name <your-email@example.com>

# Telegram notification settings
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id

# CORS settings
CORS_ALLOWED_ORIGINS=https://example.com
```

This structure provides a solid foundation for transforming the static site into a dynamic Django website following the HackSoftware Django-Styleguide.
