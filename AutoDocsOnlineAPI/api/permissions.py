from rest_framework import permissions


class IsOwnerOrReadOnlyPermission(permissions.BasePermission):
    """
    True for all safe method, if method not is safe
    then return true if user is author or has a token.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsOwnerOrObjIsPublic(permissions.BasePermission):
    """
    Work with models with field 'public'.
    return True if user is owner or document is public.
    """

    def has_object_permission(self, request, view, obj):
        return (
            obj.owner == request.user
            or obj.public
        )
