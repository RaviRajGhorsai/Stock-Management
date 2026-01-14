from rest_framework.permissions import BasePermission

class IsSuperAdminUser(BasePermission):
    """
    Allows access only to super admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser

class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin_user()


class IsAdminOrStaffUser(BasePermission):
    """
    Allows access to admin or staff users.
    """
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (user.is_admin_user() or user.is_staff_user())
