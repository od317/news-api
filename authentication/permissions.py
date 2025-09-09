from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    """
    Custom permission to only allow super admins to access the view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_super_admin

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admins (including super admins) to access the view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin