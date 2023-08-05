from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    True for all safe method, if method not is safe
    then return true if user is author or has a token.
    """

    message = 'You cannot edit an object if you are not its author.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
