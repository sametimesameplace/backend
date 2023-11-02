from rest_framework import permissions


class SuperOrReadOnly(permissions.BasePermission):
    """Allows only a superuser to create or modify.
    SAFE_METHODS are allowed for anyone.
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True
        
        return False
