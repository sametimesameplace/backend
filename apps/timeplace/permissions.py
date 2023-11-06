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


class IsAuthenticatedCreateOrSuperOrAuthor(permissions.BasePermission):
    """Allows only the author or a superuser to modify or view.
    POST is allowed for authenticated users.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.user.id == obj.user_id.id:
            return True

        return False
