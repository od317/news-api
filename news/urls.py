from django.urls import path
from . import views

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news-list'),
    path('create/', views.NewsCreateView.as_view(), name='news-create'),
    path('<int:pk>/', views.NewsDetailView.as_view(), name='news-detail'),
    path('<int:pk>/update/', views.NewsUpdateView.as_view(), name='news-update'),
    path('<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news-delete'),
    path('<int:pk>/publish/', views.publish_news, name='news-publish'),
    path('<int:pk>/unpublish/', views.unpublish_news, name='news-unpublish'),
]