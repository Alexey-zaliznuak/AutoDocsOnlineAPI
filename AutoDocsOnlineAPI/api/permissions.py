from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    """
    Return user is author.
    """

    message = 'You cannot wotk with object if you are not it`s author.'

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    True for all safe method, if method not is safe
    then return true if user is author.
    """

    message = 'You cannot edit an object if you are not it`s author.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class SelfRelated(permissions.BasePermission):
    """
    True if 'user' is request user
    """

    message = 'You cannot read or edit an object it does not related with you.'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class SelfRelatedOrIsDocumentsPackageAuthor(permissions.BasePermission):
    """
    Permission for RecordViewSet.
    Return True if user is request user or
    request method is safe and you is author of document package.
    """

    message = 'You cannot read or edit an object it does not related with you.'

    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.user
            or request.user == obj.documents_package.author
        )
