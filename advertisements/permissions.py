from rest_framework.permissions import BasePermission

from users.models import UserRole


class AdvertisementUpdateDeletePermission(BasePermission):
    message = "Access denied for not admins (moderators) or not owners"

    def has_object_permission(self, request, view, obj):
        if request.user.role == UserRole.MODERATOR or \
                request.user.role == UserRole.ADMIN or request.user.id == obj.author_id:
            return True
        return False


class SelectionUpdateDeletePermission(BasePermission):
    message = "Access denied for not owners"

    def has_object_permission(self, request, view, obj):
        if request.user.id == obj.owner_id:
            return True
        return False
