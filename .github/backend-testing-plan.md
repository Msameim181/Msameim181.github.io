# Backend Testing Plan

This document outlines the comprehensive testing strategy for the Django backend of the portfolio website, including test cases, coverage goals, and execution strategy.

## Test Structure

The test suite is organized according to the Django apps structure, with test files named using the pattern `test_*.py` in each app's directory:

```
apps/
├── profile/
│   ├── tests/
│   │   ├── test_models.py
│   │   ├── test_serializers.py
│   │   └── test_apis.py
├── resume/
│   ├── tests/
│   │   ├── test_models.py
│   │   ├── test_serializers.py
│   │   └── test_apis.py
... (similar structure for other apps)
```

## Test Cases by Component

### 1. Model Tests

Each model should have comprehensive tests covering:

#### 1.1 Profile Model Tests

- [x] `test_profile_model_creation`: Verify profile can be created with all fields
- [ ] `test_profile_str_representation`: Test string representation
- [ ] `test_profile_required_fields`: Verify required fields validation
- [ ] `test_profile_field_types`: Verify field types are correct
- [ ] `test_profile_field_constraints`: Test max length and other constraints

#### 1.2 Education Model Tests

- [ ] `test_education_model_creation`: Verify education entry can be created
- [ ] `test_education_str_representation`: Test string representation
- [ ] `test_education_ordering`: Verify entries are ordered correctly
- [ ] `test_education_date_constraints`: Test start/end date validation
- [ ] `test_education_required_fields`: Verify required fields validation

#### 1.3 Experience Model Tests

- [ ] `test_experience_model_creation`: Verify experience entry can be created
- [ ] `test_experience_str_representation`: Test string representation
- [ ] `test_experience_ordering`: Verify entries are ordered correctly
- [ ] `test_experience_date_constraints`: Test start/end date validation
- [ ] `test_experience_required_fields`: Verify required fields validation

#### 1.4 Skill Model Tests

- [ ] `test_skill_category_creation`: Verify skill category can be created
- [ ] `test_skill_creation`: Verify skill can be created with category
- [ ] `test_skill_proficiency_validation`: Test proficiency range validation
- [ ] `test_skill_category_relation`: Test relationship between skill and category
- [ ] `test_skill_ordering`: Verify skills are ordered correctly within category

#### 1.5 Project Model Tests

- [ ] `test_project_category_creation`: Verify project category can be created
- [ ] `test_project_creation`: Verify project can be created
- [ ] `test_project_slug_generation`: Test automatic slug generation
- [ ] `test_project_category_relation`: Test M2M relationship with categories
- [ ] `test_project_image_relation`: Test one-to-many relationship with images
- [ ] `test_project_ordering`: Verify projects are ordered by completion date

#### 1.6 Testimonial Model Tests

- [ ] `test_testimonial_creation`: Verify testimonial can be created
- [ ] `test_testimonial_str_representation`: Test string representation
- [ ] `test_testimonial_ordering`: Verify testimonials are ordered correctly
- [ ] `test_testimonial_rating_validation`: Test rating range validation

#### 1.7 Blog Model Tests

- [ ] `test_blog_category_creation`: Verify blog category can be created
- [ ] `test_blog_post_creation`: Verify blog post can be created
- [ ] `test_blog_slug_generation`: Test automatic slug generation
- [ ] `test_comment_creation`: Verify comment can be created
- [ ] `test_blog_category_relation`: Test M2M relationship with categories
- [ ] `test_comment_relation`: Test one-to-many relationship with comments
- [ ] `test_blog_post_ordering`: Verify posts are ordered by published date

#### 1.8 Contact Model Tests

- [ ] `test_contact_creation`: Verify contact submission can be created
- [ ] `test_contact_str_representation`: Test string representation
- [ ] `test_contact_status_choices`: Test status choices validation
- [ ] `test_contact_ordering`: Verify contacts are ordered by creation date

### 2. Serializer Tests

Each model serializer should have tests covering:

#### 2.1 Profile Serializer Tests

- [ ] `test_profile_serialization`: Verify profile is serialized correctly
- [ ] `test_profile_deserialization`: Verify profile can be deserialized
- [ ] `test_profile_validation`: Test field validation in serializer

#### 2.2 Education Serializer Tests

- [ ] `test_education_serialization`: Verify education is serialized correctly
- [ ] `test_education_deserialization`: Verify education can be deserialized
- [ ] `test_education_date_validation`: Test date field validation

#### 2.3 Experience Serializer Tests

- [ ] `test_experience_serialization`: Verify experience is serialized correctly
- [ ] `test_experience_deserialization`: Verify experience can be deserialized
- [ ] `test_experience_date_validation`: Test date field validation

#### 2.4 Skills Serializer Tests

- [ ] `test_skill_category_serialization`: Verify skill category is serialized correctly
- [ ] `test_skill_serialization`: Verify skill is serialized correctly
- [ ] `test_skill_category_nesting`: Test nested serialization of skills in category
- [ ] `test_skill_proficiency_validation`: Test proficiency validation

#### 2.5 Project Serializer Tests

- [ ] `test_project_category_serialization`: Verify project category is serialized correctly
- [ ] `test_project_serialization`: Verify project is serialized correctly
- [ ] `test_project_image_serialization`: Verify project images are serialized correctly
- [ ] `test_project_nested_serialization`: Test nested serialization of categories and images

#### 2.6 Testimonial Serializer Tests

- [ ] `test_testimonial_serialization`: Verify testimonial is serialized correctly
- [ ] `test_testimonial_deserialization`: Verify testimonial can be deserialized
- [ ] `test_testimonial_rating_validation`: Test rating validation

#### 2.7 Blog Serializer Tests

- [ ] `test_blog_category_serialization`: Verify blog category is serialized correctly
- [ ] `test_blog_post_serialization`: Verify blog post is serialized correctly
- [ ] `test_comment_serialization`: Verify comment is serialized correctly
- [ ] `test_blog_post_nested_serialization`: Test nested serialization of categories and comments

#### 2.8 Contact Serializer Tests

- [ ] `test_contact_serialization`: Verify contact is serialized correctly
- [ ] `test_contact_deserialization`: Verify contact can be deserialized
- [ ] `test_contact_email_validation`: Test email validation

### 3. API Tests

Each API endpoint should have tests covering:

#### 3.1 Profile API Tests

- [ ] `test_profile_list`: Verify GET /api/profiles/ returns profile list
- [ ] `test_profile_detail`: Verify GET /api/profiles/1/ returns profile details
- [ ] `test_profile_create_unauthorized`: Verify POST is protected
- [ ] `test_profile_create_authorized`: Verify admin can create profile
- [ ] `test_profile_update`: Verify PUT/PATCH updates profile
- [ ] `test_profile_delete`: Verify DELETE removes profile

#### 3.2 Education API Tests

- [ ] `test_education_list`: Verify GET /api/education/ returns education list
- [ ] `test_education_detail`: Verify GET /api/education/1/ returns education details
- [ ] `test_education_create_unauthorized`: Verify POST is protected
- [ ] `test_education_create_authorized`: Verify admin can create education entry
- [ ] `test_education_update`: Verify PUT/PATCH updates education entry
- [ ] `test_education_delete`: Verify DELETE removes education entry

#### 3.3 Experience API Tests

- [ ] `test_experience_list`: Verify GET /api/experience/ returns experience list
- [ ] `test_experience_detail`: Verify GET /api/experience/1/ returns experience details
- [ ] `test_experience_create_unauthorized`: Verify POST is protected
- [ ] `test_experience_create_authorized`: Verify admin can create experience entry
- [ ] `test_experience_update`: Verify PUT/PATCH updates experience entry
- [ ] `test_experience_delete`: Verify DELETE removes experience entry

#### 3.4 Skills API Tests

- [ ] `test_skill_category_list`: Verify GET /api/skill-categories/ returns category list
- [ ] `test_skill_list`: Verify GET /api/skills/ returns skill list
- [ ] `test_skill_filtering`: Verify filtering by category works
- [ ] `test_skill_category_detail`: Verify GET /api/skill-categories/1/ returns details
- [ ] `test_skill_detail`: Verify GET /api/skills/1/ returns skill details
- [ ] `test_skill_create_unauthorized`: Verify POST is protected
- [ ] `test_skill_create_authorized`: Verify admin can create skill

#### 3.5 Project API Tests

- [ ] `test_project_category_list`: Verify GET /api/project-categories/ returns category list
- [ ] `test_project_list`: Verify GET /api/projects/ returns project list
- [ ] `test_project_filtering`: Verify filtering by category and featured works
- [ ] `test_project_search`: Verify search functionality
- [ ] `test_project_detail`: Verify GET /api/projects/1/ returns project details
- [ ] `test_project_create_unauthorized`: Verify POST is protected
- [ ] `test_project_create_authorized`: Verify admin can create project
- [ ] `test_project_image_upload`: Verify image upload functionality

#### 3.6 Testimonial API Tests

- [ ] `test_testimonial_list`: Verify GET /api/testimonials/ returns testimonial list
- [ ] `test_testimonial_filtering`: Verify filtering by active status works
- [ ] `test_testimonial_detail`: Verify GET /api/testimonials/1/ returns testimonial details
- [ ] `test_testimonial_create_unauthorized`: Verify POST is protected
- [ ] `test_testimonial_create_authorized`: Verify admin can create testimonial

#### 3.7 Blog API Tests

- [ ] `test_blog_category_list`: Verify GET /api/blog-categories/ returns category list
- [ ] `test_blog_post_list`: Verify GET /api/blog-posts/ returns blog post list
- [ ] `test_blog_post_filtering`: Verify filtering by category works
- [ ] `test_blog_post_search`: Verify search functionality
- [ ] `test_blog_post_detail`: Verify GET /api/blog-posts/1/ returns post details
- [ ] `test_blog_post_create_unauthorized`: Verify POST is protected
- [ ] `test_blog_post_create_authorized`: Verify admin can create blog post
- [ ] `test_comment_create`: Verify comment can be created by anonymous user
- [ ] `test_comment_approval`: Verify comment approval process

#### 3.8 Contact API Tests

- [ ] `test_contact_form_submission`: Verify contact form submission works
- [ ] `test_contact_form_validation`: Verify form validation
- [ ] `test_contact_list_protected`: Verify GET /api/contacts/ is protected
- [ ] `test_contact_detail_protected`: Verify GET /api/contacts/1/ is protected

### 4. Admin Tests

Tests for Django admin functionality:

- [ ] `test_admin_login`: Verify admin login works
- [ ] `test_admin_models_registered`: Verify all models are registered in admin
- [ ] `test_admin_customizations`: Verify admin customizations work
- [ ] `test_admin_list_views`: Test list views for models
- [ ] `test_admin_change_views`: Test change views for models
- [ ] `test_admin_filters`: Test admin filters
- [ ] `test_admin_search`: Test admin search functionality
- [ ] `test_admin_image_upload`: Test image uploads in admin

### 5. Integration Tests

Tests covering integration points:

- [ ] `test_contact_email_notification`: Verify email is sent on contact form submission
- [ ] `test_ckeditor_integration`: Verify CKEditor works for rich text fields
- [ ] `test_image_optimization`: Verify image optimization works
- [ ] `test_vue_api_integration`: Verify Vue.js can call API endpoints
- [ ] `test_cors_configuration`: Verify CORS configuration works
- [ ] `test_authentication_flow`: Verify JWT authentication flow

### 6. Security Tests

Tests for security features:

- [ ] `test_api_authentication`: Verify authentication requirements
- [ ] `test_api_permissions`: Verify permission requirements
- [ ] `test_csrf_protection`: Verify CSRF protection works
- [ ] `test_ssl_redirect`: Verify SSL redirect works in production
- [ ] `test_password_validation`: Verify password validation for admin users
- [ ] `test_rate_limiting`: Verify rate limiting for contact form

### 7. Performance Tests

Tests for performance and caching:

- [ ] `test_api_response_time`: Test API response times
- [ ] `test_database_query_count`: Test database query efficiency
- [ ] `test_cache_effectiveness`: Test caching effectiveness
- [ ] `test_image_loading_performance`: Test image loading performance

## Test Coverage Goals

The testing strategy aims to achieve:

1. **Line Coverage**: Minimum 80% line coverage across all Python modules
2. **Branch Coverage**: Minimum 70% branch coverage
3. **Critical Path Coverage**: 100% coverage of authentication, permissions, and data validation code
4. **API Endpoint Coverage**: 100% coverage of all API endpoints

## Testing Tools

1. **pytest**: Primary testing framework
2. **pytest-django**: Django integration for pytest
3. **pytest-cov**: Code coverage reporting
4. **factory_boy**: Test data generation
5. **faker**: Fake data generation
6. **django-test-plus**: Convenience utilities for testing Django

## Test Execution

### Local Development

```bash
# Run all tests
python manage.py test

# Run tests with coverage
pytest --cov=apps

# Run specific test module
pytest apps/profile/tests/test_models.py

# Run specific test class
pytest apps/profile/tests/test_models.py::TestProfileModel

# Run specific test
pytest apps/profile/tests/test_models.py::TestProfileModel::test_profile_creation
```

### CI/CD Pipeline

Tests are automatically run in the CI/CD pipeline on every push to the main branch and pull request:

1. **Linting**: Run flake8 and black for code style checking
2. **Unit Tests**: Run all unit tests
3. **Integration Tests**: Run integration tests
4. **Coverage Report**: Generate and publish coverage report
5. **Documentation Check**: Verify API documentation generation

## Progress Tracking

- [ ] Test structure setup - 0%
- [ ] Model tests implementation - 0% 
- [ ] Serializer tests implementation - 0%
- [ ] API tests implementation - 0%
- [ ] Admin tests implementation - 0%
- [ ] Integration tests implementation - 0%
- [ ] Security tests implementation - 0%
- [ ] Performance tests implementation - 0%
- [ ] Coverage report configuration - 0%
- [ ] CI/CD pipeline integration - 0%
