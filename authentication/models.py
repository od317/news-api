from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPES = (
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.user_type})"
    
    @property
    def is_super_admin(self):
        return self.user_type == 'super_admin'
    
    @property
    def is_admin(self):
        return self.user_type in ['admin', 'super_admin']