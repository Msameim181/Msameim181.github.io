# Converting Static Site to Dynamic Django Website with Vue.js Frontend

This repository contains a personal portfolio website currently implemented as a static HTML site with some basic server functionality (FastAPI for contact form). The goal is to convert it into a fully dynamic website with a Django-based backend/admin panel that follows the [HackSoftware Django-Styleguide](https://github.com/HackSoftware/Django-Styleguide) and a modern Vue.js frontend for enhanced user experience.

## Back-End Development Plan & Progress Tracking

### Phase 1: Project Setup & Configuration ⏳
- [ ] Create Django project structure following HackSoftware styleguide
  - Test: Verify project structure matches the guidelines with proper directory organization
- [ ] Set up project settings (base, local, production)
  - Test: Verify settings work for different environments with `python manage.py check`
- [ ] Configure Docker environment for development
  - Test: Verify Docker builds and runs successfully with `docker-compose up`
- [ ] Set up CI/CD pipeline with GitHub Actions
  - Test: Verify pipeline runs on push to main branch

### Phase 2: Core Models & Database ⏳
- [ ] Design and implement Profile model and API
  - Test: `test_profile_model_fields`, `test_profile_serializer`, `test_profile_api_endpoints`
- [ ] Design and implement Education model and API
  - Test: `test_education_model_fields`, `test_education_serializer`, `test_education_api_endpoints`
- [ ] Design and implement Experience model and API
  - Test: `test_experience_model_fields`, `test_experience_serializer`, `test_experience_api_endpoints`
- [ ] Design and implement Skills model and API
  - Test: `test_skills_model_fields`, `test_skills_serializer`, `test_skills_api_endpoints`
- [ ] Design and implement Project model and API
  - Test: `test_project_model_fields`, `test_project_serializer`, `test_project_api_endpoints`
- [ ] Design and implement Testimonial model and API
  - Test: `test_testimonial_model_fields`, `test_testimonial_serializer`, `test_testimonial_api_endpoints`
- [ ] Design and implement BlogPost model and API
  - Test: `test_blogpost_model_fields`, `test_blogpost_serializer`, `test_blogpost_api_endpoints`
- [ ] Design and implement Contact model and API
  - Test: `test_contact_model_fields`, `test_contact_serializer`, `test_contact_api_endpoints`

### Phase 3: Admin Interface ⏳
- [ ] Configure and customize Django admin interface
  - Test: Verify admin interface loads and displays models
- [ ] Implement CKEditor for rich text fields
  - Test: Verify rich text editor works in admin interface
- [ ] Add image upload capabilities and optimization
  - Test: `test_image_upload`, `test_image_optimization`
- [ ] Create custom admin views for content management
  - Test: `test_custom_admin_views`

### Phase 4: API Development ⏳
- [ ] Implement RESTful API endpoints for all models
  - Test: Comprehensive API tests for all endpoints
- [ ] Configure Django REST Framework with proper serializers
  - Test: `test_api_serializers`
- [ ] Set up authentication and permissions
  - Test: `test_api_authentication`, `test_api_permissions`
- [ ] Implement filtering, pagination, and search
  - Test: `test_api_filtering`, `test_api_pagination`, `test_api_search`

### Phase 5: Contact Form Migration ⏳
- [ ] Migrate FastAPI contact form to Django
  - Test: `test_contact_form_submission`
- [ ] Implement email notification system
  - Test: `test_email_notifications`
- [ ] Set up form validation and anti-spam measures
  - Test: `test_form_validation`, `test_spam_protection`

### Phase 6: Data Migration ⏳
- [ ] Create data migration scripts for existing content
  - Test: Verify data migration with sample data
- [ ] Implement fixtures for initial data
  - Test: `test_fixtures_loading`

### Phase 7: Testing & Documentation ⏳
- [ ] Set up comprehensive test suite with pytest
  - Test: Verify test coverage is above 80%
- [ ] Create API documentation with drf-spectacular or similar
  - Test: Verify API documentation is accessible and accurate
- [ ] Document backend architecture and deployment
  - Test: Review documentation for completeness

### Phase 8: Integration & Deployment ⏳
- [ ] Set up Vue.js and Django integration
  - Test: Verify API calls from Vue.js to Django work correctly
- [ ] Configure static file serving for production
  - Test: Verify static files are served correctly
- [ ] Set up database for production
  - Test: Verify database migrations work in production
- [ ] Implement caching mechanisms
  - Test: `test_cache_performance`
- [ ] Deploy to production environment
  - Test: Verify application works in production

## Project Architecture

### Current Structure
- Static HTML pages (index.html, resume.html, contact.html, etc.)
- Assets folder with JS, CSS, images
- Simple FastAPI server for contact form processing

### Target Structure
- Django application with RESTful API endpoints
- Vue.js frontend components for dynamic content and interactions
- Admin panel for content management
- Database models for all content sections
- Django templates as base structure with Vue.js component mounting points

## Key Components to Implement

1. **Django Models**
   - `Profile`: Personal information, social links, contact details
   - `Education`: Academic history items
   - `Experience`: Work experience items  
   - `Skill`: Technical skills with proficiency levels
   - `Project`: Portfolio projects with images and categories
   - `Testimonial`: Client/colleague testimonials
   - `BlogPost`: Blog entries with comments
   - `Contact`: Contact form submissions

2. **Dynamic Content Sections**
   - About section with personal info and intro text
   - Resume section with education and experience
   - Skills section with proficiency indicators
   - Portfolio with filterable projects
   - Testimonials carousel
   - Blog with posts and comments
   - Contact form with map integration

3. **Admin Management Panel**
   - Custom Django admin interface for all content sections
   - Rich text editing (CKEditor) for longer content
   - Image upload and management
   - User authentication and permissions

## Development Guidelines

- Follow [HackSoftware Django-Styleguide](https://github.com/HackSoftware/Django-Styleguide) conventions
- Organize code in apps: `accounts`, `profile`, `portfolio`, `blog`, `contact`
- Use class-based views and Django REST Framework for APIs
- Implement proper validation for all form inputs
- Maintain current visual design and UX when converting to templates
- Optimize image handling and storage
- Set up automated testing for models and views

## Commands and Workflows

**Setup Development Environment:**
```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

**Database Models:**
- Use Django migrations for schema changes
- Define proper relationships between models
- Implement proper validation in model fields

**Templates:**
- Convert HTML files to Django templates
- Use template inheritance with a base template
- Implement template fragments for reusable components

**Static Files:**
- Organize static files according to Django conventions
- Use Django's static file handling for assets
- Implement proper image optimization and resizing

## Key Files and Directories

- `mysite/` - Main Django project directory
- `mysite/settings/` - Split settings (base.py, local.py, production.py)
- `apps/` - Django applications directory
- `apps/profile/` - Personal profile management app
- `apps/portfolio/` - Portfolio projects app
- `apps/blog/` - Blog posts app
- `apps/contact/` - Contact form processing app
- `templates/` - Django templates directory
- `static/` - Static assets directory
- `media/` - User uploaded files directory

## Deployment

- Use Docker for containerization (existing Dockerfile and docker-compose.yml)
- Configure Django settings for production environment
- Set up proper static file serving
- Configure database for production
- Implement caching for improved performance

## Security Considerations

- Secure user authentication for admin panel
- Implement CSRF protection
- Configure proper CORS settings
- Sanitize user input, especially for contact form
- Use environment variables for sensitive configuration
