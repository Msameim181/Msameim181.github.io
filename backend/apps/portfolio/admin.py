from django.contrib import admin
from apps.portfolio.models import ProjectCategory, Project, ProjectImage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ('image', 'caption', 'is_cover', 'order')


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Display', {
            'fields': ('order',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'start_date', 'end_date', 'is_featured')
    list_filter = ('category', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description', 'content')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProjectImageInline]
    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'slug', 'category', 'client')
        }),
        ('Content', {
            'fields': ('description', 'content', 'technologies')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date')
        }),
        ('Media', {
            'fields': ('cover_image',)
        }),
        ('URLs', {
            'fields': ('website_url', 'github_url')
        }),
        ('Display', {
            'fields': ('is_featured', 'order')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
