from rest_framework import permissions
from rest_framework.permissions import BasePermission
from functools import wraps
from rest_framework import permissions

class RolePermission(permissions.BasePermission):
    def __init__(self, allowed_roles=None):
        self.allowed_roles = allowed_roles or []

    def has_permission(self, request, view):
        # Ensure user is authenticated
        if not request.user.is_authenticated:
            return False

        # Check if user's role matches any allowed role
        return request.user.roles in self.allowed_roles

def role_required(roles):
    def decorator(view_class):
        view_class.permission_classes = [lambda: RolePermission(roles)]
        return view_class
    return decorator


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'roles', None) == 'admin'


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'roles', None) == 'manager'


class IsVeterinarian(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'roles', None) == 'veterinarian'
