from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import News, Resource
from .serializers import NewsSerializer, NewsListSerializer, ResourceSerializer
from authentication.permissions import IsAdmin, IsSuperAdmin
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

class NewsListView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        # Get only published news for public, all for admins
        if request.user.is_authenticated and request.user.is_admin:
            news = News.objects.all()
        else:
            news = News.objects.filter(is_published=True)
        
        serializer = NewsListSerializer(news, many=True)
        return Response(serializer.data)

class NewsDetailView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        
        # Check if user can view unpublished news
        if not news.is_published and not (request.user.is_authenticated and request.user.is_admin):
            return Response(
                {'error': 'News article not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = NewsSerializer(news)
        return Response(serializer.data)

class NewsCreateView(APIView): 
    parser_classes = [JSONParser, MultiPartParser, FormParser]  # FIXED: Added JSONParser
    permission_classes = [IsAdmin]  # Both admin and super admin can create
    
    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            # Set the author to the current user
            news = serializer.save(author=request.user)
            return Response(
                NewsSerializer(news).data, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsUpdateView(APIView):
    permission_classes = [IsAdmin]
    parser_classes = [JSONParser, MultiPartParser, FormParser]  # Added JSONParser here too
    
    def put(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        serializer = NewsSerializer(news, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsDeleteView(APIView):
    permission_classes = [IsAdmin]
    
    def delete(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        news.delete()
        return Response(
            {'message': 'News article deleted successfully'}, 
            status=status.HTTP_204_NO_CONTENT
        )

@api_view(['POST'])
@permission_classes([IsAdmin])
def publish_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    news.is_published = True
    news.save()
    return Response(
        {'message': 'News article published successfully'}, 
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([IsAdmin])
def unpublish_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    news.is_published = False
    news.save()
    return Response(
        {'message': 'News article unpublished successfully'}, 
        status=status.HTTP_200_OK
    )