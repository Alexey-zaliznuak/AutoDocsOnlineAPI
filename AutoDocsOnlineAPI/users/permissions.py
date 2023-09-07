from rest_framework import permissions
from users.models import User


class EmailConfirmed(permissions.BasePermission):
    """
    Get user by username and return True if he confirmed email
    """

    message = 'Account with this username and confirmed email not found.'

    def has_permission(self, request, view):
        q = User.objects.filter(username=request.data.get('username'))
        return q.exists() and q.get().email_confirmed
