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
