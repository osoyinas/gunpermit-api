from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allows read-only access to authenticated users.
    Only administrators can make changes (edit or delete).
    """
    
    def has_permission(self, request, view):
        # Todos los usuarios autenticados pueden ver (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        # Solo los administradores pueden editar (POST, PUT, PATCH, DELETE)
        return request.user.is_staff
