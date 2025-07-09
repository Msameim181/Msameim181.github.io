# Portfolio Backend

This is the Django backend for the dynamic portfolio website.

## Setup Instructions

### Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/Msameim181/Msameim181.github.io.git
   cd Msameim181.github.io/backend
   ```

2. Setup the environment:
   ```bash
   # Create a .env file from the example
   cp .env.example .env
   
   # Create a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

### Using Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/Msameim181/Msameim181.github.io.git
   cd Msameim181.github.io/backend
   ```

2. Setup environment:
   ```bash
   cp .env.example .env
   ```

3. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

4. Create superuser:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## API Documentation

Once the server is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/
- Schema: http://localhost:8000/api/schema/

## Testing

Run tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=apps
```

## Apps Structure

- **profile**: Personal profile information
- **resume**: Education and work experience
- **skills**: Technical skills with proficiency levels
- **portfolio**: Projects and portfolio items
- **testimonials**: Client testimonials
- **blog**: Blog posts and comments
- **contact**: Contact form submissions

## License

[MIT License](LICENSE)
