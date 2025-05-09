from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.user == request.user

class IsFileOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a file to access it.
    """
    def has_permission(self, request, view):
        # Only authenticated users can access files
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Only the owner can access their files
        return obj.user == request.user

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Пользователь может читать чужой объект, но менять — только свой.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user