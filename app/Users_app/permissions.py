from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.roles == 'admin'

class IsVeterinarian(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.roles == 'vets'

class Manager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.roles == 'manager'

