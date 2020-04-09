"""Ride Permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsNotRideOwner(BasePermission):
    """Only users that are not the ride's owner can join rides."""

    def has_object_permission(self, request, view, obj):
        """Verify requesting user is not the ride's owner."""
        return not request.user == obj.offered_by

class IsRideOwner(BasePermission):
    """Verify requesting user is the ride creator."""

    def has_object_permission(self, request, view, obj):
        """Verify that the requesting user is the ride creator."""
        return request.user == obj.offered_by
