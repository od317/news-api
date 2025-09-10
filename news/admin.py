from django.contrib import admin
from .models import News, Resource

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'created_at']
    search_fields = ['title', 'link']

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'published_at', 'created_at']
    list_filter = ['is_published', 'created_at', 'published_at']
    search_fields = ['title', 'body']
    filter_horizontal = ['resources']