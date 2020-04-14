"""Circle Premission Class."""

# Django
from rest_framework.permissions import BasePermission

# Models
from cride.circles.models import Membership


class IsCircleAdmin(BasePermission):
    """Allow access only to circle admins."""

    def has_object_permisssions(self, request, view, obj):
        """Verify user has a membership in the object (circle)"""
        try:
            Membership.objects.get(
                user=request.user,
                circle=obj,
                is_admin=True,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True
