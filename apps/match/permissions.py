from rest_framework import permissions


class SuperOrAuthors(permissions.BasePermission):
    """Allows superuser or either owner of a match to access."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        
        if request.user.id == obj.timeplace_1.user.id:
            return True

        if request.user.id == obj.timeplace_2.user.id:
            return True

        return False
