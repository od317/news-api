from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Investigation, InvestigationPage
from .serializers import (
    InvestigationSerializer, 
    InvestigationListSerializer, 
    InvestigationPageSerializer
)
from authentication.permissions import IsAdmin

class InvestigationPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class InvestigationListView(APIView):
    permission_classes = [permissions.AllowAny]
    pagination_class = InvestigationPagination
    
    def get(self, request):
        # Get only published investigations for public, all for admins
        if request.user.is_authenticated and request.user.is_admin:
            investigations = Investigation.objects.all()
        else:
            investigations = Investigation.objects.filter(is_published=True)
        
        # Paginate results
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(investigations, request)
        
        serializer = InvestigationListSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class InvestigationDetailView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, pk):
        investigation = get_object_or_404(Investigation, pk=pk)
        
        # Check if user can view unpublished investigation
        if not investigation.is_published and not (request.user.is_authenticated and request.user.is_admin):
            return Response(
                {'error': 'Investigation not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = InvestigationSerializer(investigation)
        return Response(serializer.data)

class InvestigationPagesView(APIView):
    permission_classes = [permissions.AllowAny]
    pagination_class = InvestigationPagination
    
    def get(self, request, investigation_pk):
        investigation = get_object_or_404(Investigation, pk=investigation_pk)
        
        # Check if user can view unpublished investigation
        if not investigation.is_published and not (request.user.is_authenticated and request.user.is_admin):
            return Response(
                {'error': 'Investigation not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        pages = investigation.pages.all()
        
        # Paginate results
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(pages, request)
        
        serializer = InvestigationPageSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

# Admin views
class InvestigationCreateView(APIView):
    permission_classes = [IsAdmin]
    
    def post(self, request):
        serializer = InvestigationSerializer(data=request.data)
        if serializer.is_valid():
            investigation = serializer.save()
            return Response(
                InvestigationSerializer(investigation).data, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InvestigationPageCreateView(APIView):
    permission_classes = [IsAdmin]
    
    def post(self, request, investigation_pk):
        investigation = get_object_or_404(Investigation, pk=investigation_pk)
        
        # Calculate next page number
        next_page_number = investigation.pages.count() + 1
        
        data = request.data.copy()
        data['page_number'] = next_page_number
        
        serializer = InvestigationPageSerializer(data=data)
        if serializer.is_valid():
            page = serializer.save(investigation=investigation)
            return Response(
                InvestigationPageSerializer(page).data, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAdmin])
def publish_investigation(request, pk):
    investigation = get_object_or_404(Investigation, pk=pk)
    investigation.is_published = True
    investigation.save()
    return Response(
        {'message': 'Investigation published successfully'}, 
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([IsAdmin])
def unpublish_investigation(request, pk):
    investigation = get_object_or_404(Investigation, pk=pk)
    investigation.is_published = False
    investigation.save()
    return Response(
        {'message': 'Investigation unpublished successfully'}, 
        status=status.HTTP_200_OK
    )