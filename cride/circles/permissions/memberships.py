"""Membership Permission Classes."""

# Django
from rest_framework.permissions import BasePermission

# Models
from cride.circles.models import Membership


class IsActiveCircleMember(BasePermission):
    """Allow access only to circle members.

    Excpects that the views implementing this permission
    have a 'circle' atttribute assigned.
    """

    def has_permission(self, resquest, view):
        """Verifies user is an active member of the circle."""

        try:
            Membership.objects.get(
                user=resquest.user,
                circle=view.circle,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True


class IsSelfMember(BasePermission):
    """
    Allows access to invitations details only to the owner of the information.
    """

    def has_permission(self, request, view):
        """Let object permission grant access."""
        obj = view.get_object()
        return self.has_object_permission(request, view, obj)

    def has_object_permission(self, request, view, obj):
        """Allow access only if member is owned by the requesting user."""
        return request.user == obj.user
        
