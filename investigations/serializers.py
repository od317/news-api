from rest_framework import serializers
from .models import Investigation, InvestigationPage

class InvestigationPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestigationPage
        fields = [
            'id', 'page_number', 'title', 'content', 
            'image', 'source', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class InvestigationSerializer(serializers.ModelSerializer):
    pages = InvestigationPageSerializer(many=True, read_only=True)
    total_pages = serializers.SerializerMethodField()
    
    class Meta:
        model = Investigation
        fields = [
            'id', 'title', 'description', 'pages', 'total_pages',
            'is_published', 'published_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_pages']
    
    def get_total_pages(self, obj):
        return obj.pages.count()

class InvestigationListSerializer(serializers.ModelSerializer):
    total_pages = serializers.SerializerMethodField()
    first_page_preview = serializers.SerializerMethodField()
    
    class Meta:
        model = Investigation
        fields = [
            'id', 'title', 'description', 'total_pages',
            'first_page_preview', 'published_at', 'created_at'
        ]
        read_only_fields = fields
    
    def get_total_pages(self, obj):
        return obj.pages.count()
    
    def get_first_page_preview(self, obj):
        first_page = obj.pages.first()
        if first_page:
            return first_page.content[:200] + '...' if len(first_page.content) > 200 else first_page.content
        return ""