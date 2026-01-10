from rest_framework.permissions import BasePermission

class IsSuperAdminUser(BasePermission):
    """
    Allows access only to super admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser

