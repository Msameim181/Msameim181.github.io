#!/bin/bash

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create Django project
django-admin startproject config .

# Create directories
mkdir -p config/settings
mkdir -p apps
mkdir -p static
mkdir -p media
mkdir -p templates

# Create __init__.py files
touch apps/__init__.py
touch config/settings/__init__.py

# Create settings files
mv config/settings.py config/settings/base.py
touch config/settings/local.py
touch config/settings/production.py
touch config/settings/test.py

# Create settings __init__.py to import from local by default
echo 'from .local import *' > config/settings/__init__.py

# Create pytest.ini
echo '[pytest]
DJANGO_SETTINGS_MODULE = config.settings.test
python_files = test_*.py
testpaths = apps
' > pytest.ini

echo "Django project structure created successfully!"
