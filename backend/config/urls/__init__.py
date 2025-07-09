"""
Common URL configuration module that imports all the individual app URL modules
to make them available for importing in the main urls.py.
This avoids circular imports and keeps the main urls.py file cleaner.
"""

from config.urls.api import urlpatterns as api_urlpatterns
from config.urls.blog import urlpatterns as blog_urlpatterns
from config.urls.contact import urlpatterns as contact_urlpatterns
from config.urls.portfolio import urlpatterns as portfolio_urlpatterns
from config.urls.testimonials import urlpatterns as testimonials_urlpatterns
