from django.urls import path
from . import views

urlpatterns = [
    # Public endpoints
    path('', views.InvestigationListView.as_view(), name='investigation-list'),
    path('<int:pk>/', views.InvestigationDetailView.as_view(), name='investigation-detail'),
    path('<int:investigation_pk>/pages/', views.InvestigationPagesView.as_view(), name='investigation-pages'),
    
    # Admin endpoints
    path('create/', views.InvestigationCreateView.as_view(), name='investigation-create'),
    path('<int:investigation_pk>/pages/create/', views.InvestigationPageCreateView.as_view(), name='investigation-page-create'),
    path('<int:pk>/publish/', views.publish_investigation, name='investigation-publish'),
    path('<int:pk>/unpublish/', views.unpublish_investigation, name='investigation-unpublish'),
]