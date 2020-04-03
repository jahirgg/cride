"""Users Premission Class."""

# Django
from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
    """Allow access to objects own by the requesting user."""

    def has_object_permisssions(self, request, view, obj):
        """Check if object and user are the username"""
        return request.user == obj
