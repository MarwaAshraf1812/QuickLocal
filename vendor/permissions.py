from rest_framework import permissions #type: ignore
from .models import Vendor


class IsStaffUser(permissions.BasePermission):
    """
    Custom permission to allow only staff users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff