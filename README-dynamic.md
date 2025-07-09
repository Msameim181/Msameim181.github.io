# Dynamic Portfolio Website with Django

This repository contains a personal portfolio website that is being converted from a static HTML site to a fully dynamic Django-based website with a content management system. The goal is to make all content sections editable through an admin panel while maintaining the current design and user experience.

## Project Overview

The website includes the following main sections:
- About Me / Profile
- Resume (Education, Experience, Skills)
- Portfolio Projects
- Blog (optional)
- Testimonials
- Contact Form

## Current Structure

- Static HTML pages with hardcoded content
- Simple FastAPI backend for contact form submissions
- Docker containerization for deployment

## Target Structure

- Django application with dynamic templates
- Admin panel for content management
- PostgreSQL database for storing content
- RESTful API endpoints for frontend-backend communication

## Conversion Plan

The conversion from static to dynamic will follow these steps:

1. Set up Django project structure following [HackSoftware Django-Styleguide](https://github.com/HackSoftware/Django-Styleguide)
2. Design and implement models for all content sections
3. Create admin interfaces for content management
4. Set up Django REST Framework API endpoints
5. Configure Vue.js frontend with component structure
6. Implement Vue components for each section
7. Connect Vue components to API endpoints
8. Convert contact form to use Vue.js and Django API
9. Configure Docker for Django + Vue.js deployment
10. Set up production environment

## Technical Details

### Backend
- Django 4.2+
- Django REST Framework for API endpoints
- PostgreSQL database
- Python Telegram Bot API for notifications

### Frontend
- Vue.js for dynamic frontend components
- Django templates as the base structure
- CSS (existing styles with possible optimizations)
- API-driven content loading replacing jQuery scripts

### Deployment
- Docker and Docker Compose
- Nginx for static files and reverse proxy
- Gunicorn for Django application server

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/Msameim181/Msameim181.github.io.git
cd Msameim181.github.io
git checkout feature/dynamic
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install backend dependencies:
```bash
pip install -r requirements.txt
```

4. Install frontend dependencies:
```bash
cd frontend
npm install
```

4. Create `.env` file from example:
```bash
cp .env.example .env
# Edit .env file with your settings
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run development server:
```bash
python manage.py runserver
```

## Documentation

For more detailed information, see the following documents:

- [Conversion Instructions and System Prompt](.github/copilot-instructions.md)
- [Django Project Structure](.github/django-project-structure.md)
- [Implementation Plan](.github/implementation-plan.md)
- [Contact Form Migration Guide](.github/contact-form-migration.md)
- [Vue.js Integration Guide](.github/vue-integration.md)

## License

This project is licensed under the terms of the LICENSE file included in this repository.

## Author

Mohammad Mahdi Samei
- GitHub: [Msameim181](https://github.com/Msameim181)
- Website: [msameim181.github.io](https://msameim181.github.io/)
