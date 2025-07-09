from django.contrib import admin
from apps.testimonials.models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'company', 'rating', 'is_featured')
    list_filter = ('rating', 'is_featured')
    search_fields = ('name', 'position', 'company', 'content')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Testimonial Information', {
            'fields': ('name', 'position', 'company')
        }),
        ('Content', {
            'fields': ('content', 'rating')
        }),
        ('Media', {
            'fields': ('avatar',)
        }),
        ('Display', {
            'fields': ('is_featured', 'order')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
