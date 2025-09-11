from django.contrib import admin
from .models import Investigation, InvestigationPage

class InvestigationPageInline(admin.TabularInline):
    model = InvestigationPage
    extra = 1

@admin.register(Investigation)
class InvestigationAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'published_at', 'created_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'description']
    inlines = [InvestigationPageInline]

@admin.register(InvestigationPage)
class InvestigationPageAdmin(admin.ModelAdmin):
    list_display = ['investigation', 'page_number', 'title', 'created_at']
    list_filter = ['investigation', 'created_at']
    search_fields = ['title', 'content']