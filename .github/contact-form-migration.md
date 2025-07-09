# FastAPI to Django: Contact Form Migration Guide

This document provides detailed instructions for migrating the existing FastAPI contact form processing to Django while maintaining Telegram notification functionality.

## Current FastAPI Implementation

The current implementation uses FastAPI with SQLAlchemy to:
1. Accept form data (name, email, message)
2. Store the data in a SQLite database
3. Send a notification to a Telegram chat

Key components:
- `server.py`: Contains the FastAPI application and endpoints
- `contact_requests.db`: SQLite database for storing contact requests
- `.env`: Contains environment variables for Telegram bot token and chat ID

## Django Implementation Plan

### 1. Create Contact App

```bash
mkdir -p apps/contact
```

### 2. Define Contact Model

```python
# apps/contact/models.py
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

### 3. Create API Serializer

```python
# apps/contact/serializers.py
from rest_framework import serializers
from .models import ContactRequest

class ContactRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactRequest
        fields = ['full_name', 'email', 'message']
```

### 4. Implement Telegram Notification Service

```python
# apps/contact/services.py
import os
import logging
import asyncio
from telegram import Bot
from django.conf import settings
from django.utils.decorators import async_to_sync

logger = logging.getLogger(__name__)

async def send_telegram_notification_async(message):
    """Send notification to Telegram chat"""
    try:
        bot_token = settings.TELEGRAM_BOT_TOKEN
        chat_id = settings.TELEGRAM_CHAT_ID
        
        if not bot_token or not chat_id:
            logger.error("Telegram bot token or chat ID not configured")
            return False
        
        bot = Bot(token=bot_token)
        await bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")
        return True
    except Exception as e:
        logger.error(f"Failed to send Telegram notification: {e}")
        return False

def send_telegram_notification(message):
    """Synchronous wrapper for the async Telegram notification function"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(send_telegram_notification_async(message))
    loop.close()
    return result
```

### 5. Create API View

```python
# apps/contact/views.py
import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import ContactRequest
from .serializers import ContactRequestSerializer
from .services import send_telegram_notification
from django.utils.decorators import async_to_sync

logger = logging.getLogger(__name__)

class ContactViewSet(viewsets.ModelViewSet):
    queryset = ContactRequest.objects.all()
    serializer_class = ContactRequestSerializer
    http_method_names = ['post', 'get', 'head']  # Limit available methods
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Send Telegram notification (same as in original FastAPI implementation)
        try:
            full_name = serializer.validated_data['full_name']
            email = serializer.validated_data['email']
            message = serializer.validated_data['message']
            
            telegram_message = f'New contact request from "{full_name}" ({email}): \n{message}'
            send_telegram_notification(telegram_message)
        except Exception as e:
            logger.error(f"Failed to send Telegram notification: {e}")
        
        return Response({"status": "success"}, status=status.HTTP_201_CREATED)
```

### 6. Register URL Routes

```python
# apps/contact/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet

router = DefaultRouter()
router.register('', ContactViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

### 7. Configure Settings

```python
# config/settings/base.py

# Add these variables to load from environment
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
```

### 8. Update Frontend JavaScript

```javascript
// static/js/common.js
function submitForm(){
    var name = $("#nameContact").val(),
        email = $("#emailContact").val(),
        message = $("#messageContact").val();
    
    var formData = {
        full_name: name,
        email: email,
        message: message
    };

    // Get CSRF token for Django
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // Update URL to Django endpoint
    var url = "/api/contact/";
    
    $.ajax({
        type: "POST",
        url: url,
        headers: {'X-CSRFToken': csrftoken},
        contentType: 'application/json',
        data: JSON.stringify(formData),
        success : function(text){
            if (text.status === "success"){
                formSuccess();
            } else {
                formError();
                submitMSG(false,text);
            }
        },
        error: function(xhr, status, error) {
            formError();
            submitMSG(false, "Message could not be sent. Please try again.");
        }
    });
}
```

### 9. Update Contact Form Template

```html
<!-- templates/contact.html -->
<form id="contact-form" class="contact-form" data-toggle="validator">
    {% csrf_token %}
    <div class="row">
        <div class="form-group col-12 col-md-6">
            <input type="text" class="input form-control" id="nameContact" name="nameContact" placeholder="Full name" required="required" autocomplete="on" oninvalid="setCustomValidity('Fill in the field')" onkeyup="setCustomValidity('')">
            <div class="help-block with-errors"></div>
        </div>
        <div class="form-group col-12 col-md-6">
            <input type="email" class="input form-control" id="emailContact" name="emailContact" placeholder="Email address" required="required" autocomplete="on" oninvalid="setCustomValidity('Email is incorrect')" onkeyup="setCustomValidity('')">
            <div class="help-block with-errors"></div>
        </div>
        <div class="form-group col-12 col-md-12">
            <textarea class="textarea form-control" id="messageContact" name="messageContact" placeholder="Your Message" rows="4" required="required" oninvalid="setCustomValidity('Fill in the field')" onkeyup="setCustomValidity('')"></textarea>
            <div class="help-block with-errors"></div>
        </div>
    </div>
    <div class="row">
        <div class="col-12 col-md-6 order-2 order-md-1 text-center text-md-start">
            <div id="validator-contact" class="hidden"></div>
        </div>
        <div class="col-12 col-md-6 order-1 order-md-2 text-end">
            <button type="submit" class="btn"><i class="font-icon icon-send"></i> Send Message</button>
        </div>
    </div>
</form>
```

### 10. Configure Admin Interface

```python
# apps/contact/admin.py
from django.contrib import admin
from .models import ContactRequest

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('full_name', 'email', 'message')
    readonly_fields = ('full_name', 'email', 'message', 'created_at')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        if obj and not obj.is_read:
            # Allow marking as read
            return True
        return False
    
    def save_model(self, request, obj, form, change):
        if not change:
            return
        if 'is_read' in form.changed_data:
            obj.save()
```

### 11. Data Migration from SQLite to Django

Create a management command to import existing contact requests:

```python
# apps/contact/management/commands/import_contacts.py
import sqlite3
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.contact.models import ContactRequest

class Command(BaseCommand):
    help = 'Import contact requests from SQLite database'
    
    def handle(self, *args, **options):
        try:
            conn = sqlite3.connect('contact_requests.db')
            cursor = conn.cursor()
            cursor.execute("SELECT full_name, email, message FROM contact_requests")
            rows = cursor.fetchall()
            
            imported_count = 0
            for row in rows:
                full_name, email, message = row
                ContactRequest.objects.create(
                    full_name=full_name,
                    email=email,
                    message=message,
                    created_at=timezone.now(),  # Use current time as we don't have original timestamp
                    is_read=True  # Mark as read since these are old
                )
                imported_count += 1
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully imported {imported_count} contact requests')
            )
            
        except sqlite3.Error as e:
            self.stdout.write(
                self.style.ERROR(f'SQLite error: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {e}')
            )
```

### 12. Testing the Migration

Test the new Django implementation with these steps:

1. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

2. Import existing data:
```bash
python manage.py import_contacts
```

3. Test the contact form:
   - Navigate to contact page
   - Submit a test form
   - Verify data is saved to database
   - Verify Telegram notification is sent

4. Check admin interface:
   - Log in to Django admin
   - Verify contact requests are visible
   - Test marking as read functionality

## Integration with the Rest of the Dynamic Site

Once the contact form is migrated, integrate it with other dynamic features:

1. Load profile information dynamically for sidebar
2. Implement dynamic map with location from profile settings
3. Add notification counter for unread messages in admin dashboard
4. Create optional auto-reply email functionality
