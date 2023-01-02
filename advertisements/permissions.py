from rest_framework.permissions import BasePermission
from users.models import UserRole


class AdvertisementUpdateDeletePermission(BasePermission):
    message = "Access denied for not owners or admins (moderators)"

    def has_permission(self, request, view):

        if request.user.role == UserRole.MODERATOR or \
                request.user.role == UserRole.ADMIN:
            return True
        return False
