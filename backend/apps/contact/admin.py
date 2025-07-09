from django.contrib import admin
from apps.contact.models import ContactMessage, ContactInformation


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at', 'ip_address', 'user_agent')
    fieldsets = (
        ('Message Information', {
            'fields': ('name', 'email', 'subject')
        }),
        ('Content', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Metadata', {
            'fields': ('ip_address', 'user_agent', 'created_at', 'updated_at')
        }),
    )


@admin.register(ContactInformation)
class ContactInformationAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'country', 'city', 'show_on_website')
    list_filter = ('show_on_website',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Location', {
            'fields': ('address', 'city', 'state', 'country', 'postal_code')
        }),
        ('Contact', {
            'fields': ('email', 'phone')
        }),
        ('Map Coordinates', {
            'fields': ('latitude', 'longitude')
        }),
        ('Visibility', {
            'fields': ('show_on_website',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
