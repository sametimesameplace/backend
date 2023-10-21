from rest_framework import permissions


class UserSuperDeleteOnly(permissions.BasePermission):
    """Allows only the user itself or a superuser to view and modify
    a user profile. Only a superuser can delete.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True

            if request.method == "DELETE":
                return False

            if request.user.id == obj.id:
                return True

        return False


class SuperOnly(permissions.BasePermission):
    """Allows access only to superusers
    """
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False