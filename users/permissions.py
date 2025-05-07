from rest_framework import permissions

class IsSelfOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow users to edit their own profile
    or allow admin users to edit any profile.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner or admin.
        return obj == request.user or request.user.is_staff 