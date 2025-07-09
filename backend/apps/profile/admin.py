from django.contrib import admin
from apps.profile.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'title', 'email')
    search_fields = ('first_name', 'last_name', 'title', 'bio', 'email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'title', 'bio', 'avatar')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'location')
        }),
        ('Social Links', {
            'fields': ('github', 'linkedin', 'twitter', 'website')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
