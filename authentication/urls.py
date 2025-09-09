from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admins/create/', views.create_admin, name='create-admin'),
    path('admins/list/', views.list_admins, name='list-admins'),
]