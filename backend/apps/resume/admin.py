from django.contrib import admin
from apps.resume.models import Education, Experience


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'field_of_study', 'start_date', 'end_date', 'is_current', 'order')
    list_filter = ('is_current',)
    search_fields = ('institution', 'degree', 'field_of_study', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Education Information', {
            'fields': ('institution', 'degree', 'field_of_study', 'location')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'is_current')
        }),
        ('Details', {
            'fields': ('description', 'order')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('position', 'company', 'start_date', 'end_date', 'is_current', 'order')
    list_filter = ('is_current',)
    search_fields = ('company', 'position', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Experience Information', {
            'fields': ('company', 'position', 'location')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'is_current')
        }),
        ('Details', {
            'fields': ('description', 'order')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
