# System Prompt: Converting Static Portfolio to Dynamic Django Website

You are an expert Django developer tasked with converting a static personal portfolio website into a fully dynamic website with an admin management panel. Follow the HackSoftware Django-Styleguide (https://github.com/HackSoftware/Django-Styleguide) for all implementations. Your goal is to maintain the existing design and UX while making all content editable through a Django admin interface.

## Project Structure

Create a Django project with the following structure:

```
mysite/
├── config/                  # Django project configuration
│   ├── settings/            
│   │   ├── base.py          # Base settings
│   │   ├── local.py         # Development settings
│   │   └── production.py    # Production settings
│   ├── urls.py              
│   └── wsgi.py              
├── apps/                    # Django applications
│   ├── accounts/            # User authentication app
│   ├── core/                # Core functionality and shared models
│   ├── profile/             # Personal info management
│   ├── portfolio/           # Projects and work showcase
│   ├── blog/                # Blog posts management
│   └── contact/             # Contact form processing
├── templates/               # Django templates
│   ├── base.html            # Base template with common structure
│   ├── index.html           # Home page template
│   ├── resume.html          # Resume page template
│   ├── portfolio.html       # Portfolio page template
│   ├── blog.html            # Blog listing template
│   ├── single-post.html     # Blog post detail template
│   ├── contact.html         # Contact page template
│   └── includes/            # Reusable template fragments
├── static/                  # Static assets (copied from current site)
├── media/                   # User uploaded content
└── manage.py                # Django management script
```

## Data Models

Implement the following data models:

### Profile App
```python
# apps/profile/models.py
class Profile(models.Model):
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='profile/')
    position = models.CharField(max_length=100)
    bio = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    birthday = models.DateField()
    location = models.CharField(max_length=100)
    resume_file = models.FileField(upload_to='files/')
    
class SocialLink(models.Model):
    profile = models.ForeignKey(Profile, related_name='social_links')
    platform = models.CharField(max_length=50)  # linkedin, github, etc.
    url = models.URLField()
    icon = models.CharField(max_length=50)  # feathericon-linkedin, etc.

class Badge(models.Model):
    profile = models.ForeignKey(Profile, related_name='badges')
    text = models.CharField(max_length=100)  # Python Developer, etc.
```

### Experience App
```python
# apps/profile/models.py
class Education(models.Model):
    title = models.CharField(max_length=200)  # University name
    period = models.CharField(max_length=100)  # Date range
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

class Experience(models.Model):
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    period = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    
class Skill(models.Model):
    name = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)  # +2 Years Experience, etc.
    proficiency = models.IntegerField()  # 0-100 value for progress bar
    category = models.CharField(max_length=50)  # technical, language, etc.
    order = models.PositiveIntegerField(default=0)
```

### Portfolio App
```python
# apps/portfolio/models.py
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

class Project(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='projects/')
    client = models.CharField(max_length=100, blank=True)
    date = models.DateField()
    description = models.TextField()
    
class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images')
    image = models.ImageField(upload_to='projects/')
    order = models.PositiveIntegerField(default=0)
```

### Blog App
```python
# apps/blog/models.py
class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog/')
    content = models.TextField()
    pub_date = models.DateField()
    
class Comment(models.Model):
    post = models.ForeignKey(BlogPost, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    avatar = models.ImageField(upload_to='comments/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Testimonial App
```python
# apps/core/models.py
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='testimonials/')
    position = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    date = models.DateField()
    order = models.PositiveIntegerField(default=0)
    
class Client(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='clients/')
    url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
```

### Contact App
```python
# apps/contact/models.py
class ContactRequest(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
```

## Views and URLs

Use Django class-based views for all page rendering. Create API views using Django REST Framework for data that needs to be loaded asynchronously.

### Main URL patterns
```python
# config/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('portfolio/', include('apps.portfolio.urls')),
    path('blog/', include('apps.blog.urls')),
    path('contact/', include('apps.contact.urls')),
    path('api/', include('config.api_urls')),  # API endpoints
]
```

## Admin Customization

Enhance the Django admin interface for better content management:

```python
# apps/profile/admin.py
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'email', 'phone')
    
class BadgeInline(admin.TabularInline):
    model = Badge
    extra = 1
    
class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1
```

Use similar patterns for all models, with inline editing where appropriate.

## Templates

Convert the static HTML files into Django templates using template inheritance. Use the `{% include %}` tag for reusable components.

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Mohammad Mahdi Samei{% endblock %}</title>
    {% include 'includes/meta.html' %}
    
    <!-- Styles -->
    <link rel="stylesheet" href="{% static 'styles/vendors/bootstrap.min.css' %}">
    <link rel="stylesheet" href="{% static 'styles/style.css' %}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <main class="main">
        <div class="container gutter-top gutter-bottom">
            <div class="row sticky-parent">
                {% include 'includes/sidebar.html' %}
                
                <!-- Content -->
                <div class="col-12 col-md-12 col-xl-9">
                    <div class="box-outer">
                        {% include 'includes/navigation.html' %}
                        {% block content %}{% endblock %}
                    </div>
                </div>
            </div>
        </div>
    </main>
    
    <div class="back-to-top"></div>
    
    <!-- JavaScripts -->
    <script src="{% static 'js/jquery-3.4.1.min.js' %}"></script>
    <script src="{% static 'js/plugins.min.js' %}"></script>
    <script src="{% static 'js/common.js' %}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

## API Endpoints

Create RESTful API endpoints for dynamic data:

```python
# apps/contact/api.py
class ContactViewSet(viewsets.ModelViewSet):
    queryset = ContactRequest.objects.all()
    serializer_class = ContactRequestSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Send notification to Telegram (from current server.py logic)
        try:
            telegram_message = f'New contact request from "{serializer.validated_data["full_name"]}" ({serializer.validated_data["email"]}): \n{serializer.validated_data["message"]}'
            # Use Django's async capabilities to send notification
            async_task(send_telegram_notification, telegram_message)
        except Exception as e:
            logger.error(f"Failed to send Telegram notification: {e}")
        
        return Response({"status": "success"}, status=status.HTTP_201_CREATED)
```

## Frontend JavaScript

Modify the existing JavaScript to work with the Django backend:

```javascript
// static/js/common.js - modified contact form submission
function submitForm(){
    var name = $("#nameContact").val(),
        email = $("#emailContact").val(),
        message = $("#messageContact").val();
    
    var formData = {
        full_name: name,
        email: email,
        message: message
    };

    // Update to use Django's CSRF protection
    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    $.ajax({
        type: "POST",
        url: "/api/contact/",
        headers: {'X-CSRFToken': csrftoken},
        contentType: 'application/json',
        data: JSON.stringify(formData),
        success: function(response){
            formSuccess();
        },
        error: function(){
            formError();
            submitMSG(false, "Message could not be sent. Please try again.");
        }
    });
}
```

## Deployment

Modify the existing Docker setup to use Django:

```dockerfile
# Update dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run gunicorn for production
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```yaml
# Update docker-compose.yml
version: '3.7'

services:
  web:
    build: .
    restart: always
    env_file:
      - .env
    volumes:
      - ./media:/app/media
      - ./static:/app/static
    ports:
      - "6549:8000"
    depends_on:
      - db
  
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - .env
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_DB=portfolio

volumes:
  postgres_data:
```

## Requirements

Create an updated requirements.txt file:

```
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
gunicorn==21.2.0
psycopg2-binary==2.9.9
pillow==10.1.0
python-dotenv==1.0.0
python-telegram-bot==20.6
django-ckeditor==6.7.0
django-storages==1.14.2
```

## Django Settings

Follow HackSoftware Django-Styleguide for settings organization:

```python
# config/settings/base.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Splitting settings into multiple files
# Common settings here

# config/settings/local.py
from .base import *

DEBUG = True
# Development specific settings

# config/settings/production.py
from .base import *

DEBUG = False
# Production specific settings
```

## Migration and Data Import

Create a Django management command to import existing data:

```python
# apps/core/management/commands/import_initial_data.py
class Command(BaseCommand):
    help = 'Import initial data from static HTML files'
    
    def handle(self, *args, **options):
        # Parse HTML files and extract content
        # Create model instances with extracted data
```

## Testing

Set up automated testing for models and views:

```python
# apps/profile/tests.py
class ProfileModelTest(TestCase):
    def setUp(self):
        Profile.objects.create(
            name="Mohammad Mahdi Samei",
            position="Python Developer",
            email="9259samei@gmail.com",
            # other fields
        )
    
    def test_profile_creation(self):
        profile = Profile.objects.get(name="Mohammad Mahdi Samei")
        self.assertEqual(profile.email, "9259samei@gmail.com")
```

## Security

Implement proper security measures:

- Use environment variables for sensitive data
- Configure proper CORS settings
- Implement authentication for admin access
- Set up HTTPS in production
- Sanitize user inputs
- Follow Django security best practices

## Performance

Optimize for performance:

- Configure caching for templates and database queries
- Use Django's built-in optimization techniques
- Implement lazy loading for images
- Minimize and bundle frontend assets
- Configure database indexes where appropriate
