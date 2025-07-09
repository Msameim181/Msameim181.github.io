from django.contrib import admin
from apps.blog.models import Category, Tag, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'published_at', 'featured')
    list_filter = ('status', 'category', 'featured', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'subtitle', 'content', 'excerpt')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'published_at'
    filter_horizontal = ('tags',)
    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'slug', 'subtitle', 'category')
        }),
        ('Content', {
            'fields': ('content', 'excerpt')
        }),
        ('Media', {
            'fields': ('cover_image',)
        }),
        ('Tags', {
            'fields': ('tags',)
        }),
        ('Publication', {
            'fields': ('status', 'published_at', 'featured')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
