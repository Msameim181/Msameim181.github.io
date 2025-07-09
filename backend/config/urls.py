from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API authentication
    path('api-auth/', include('rest_framework.urls')),
    
    # CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    # API documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API URLs
    path('api/v1/', include([
        path('', include('config.urls.api')),
        path('portfolio/', include('config.urls.portfolio')),
        path('testimonials/', include('config.urls.testimonials')),
        path('blog/', include('config.urls.blog')),
        path('contact/', include('config.urls.contact')),
    ])),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
