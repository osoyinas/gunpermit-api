from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allows read-only access to authenticated users.
    Only administrators can make changes (edit or delete).
    """
    
    def has_permission(self, request, view):
        # All authenticated users can view (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        # Only administrators can edit (POST, PUT, PATCH, DELETE)
        return request.user.is_staff
