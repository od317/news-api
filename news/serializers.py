from rest_framework import serializers
from .models import News, Resource

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'title', 'link', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class NewsSerializer(serializers.ModelSerializer):
    resources = ResourceSerializer(many=True, required=False)
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = News
        fields = [
            'id', 'title', 'body', 'image', 'resources', 
            'author', 'author_name', 'is_published', 'published_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'published_at', 'created_at', 'updated_at']
 
    def validate(self, data):
        # Add custom validation if needed
        return data
    
    def create(self, validated_data):
        resources_data = validated_data.pop('resources', [])
        news = News.objects.create(**validated_data)
        
        # Create resources if provided
        for resource_data in resources_data:
            resource, created = Resource.objects.get_or_create(
                title=resource_data['title'],
                link=resource_data['link']
            )
            news.resources.add(resource)
        
        return news
    
    def update(self, instance, validated_data):
        resources_data = validated_data.pop('resources', None)
        
        # Update news fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update resources if provided
        if resources_data is not None:
            instance.resources.clear()
            for resource_data in resources_data:
                resource, created = Resource.objects.get_or_create(
                    title=resource_data['title'],
                    link=resource_data['link']
                )
                instance.resources.add(resource)
        
        return instance

class NewsListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    excerpt = serializers.SerializerMethodField()
    
    class Meta:
        model = News
        fields = [
            'id', 'title', 'excerpt', 'image', 'author_name',
            'published_at', 'created_at'
        ]
        read_only_fields = fields
    
    def get_excerpt(self, obj):
        return obj.body[:150] + '...' if len(obj.body) > 150 else obj.body