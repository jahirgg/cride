"""Memberships Serializer Class."""

# Django REST Framework
from rest_framework import serializers

# Serializers
from cride.users.serializers import UserModelSerializer

# Models
from cride.circles.models import Membership


class MembershipModelSerializer(serializers.ModelSerializer):
    """Membership model serializer."""

    user = UserModelSerializer(read_only=True)
    invited_by = serializers.StringRelatedField()
    joined_at = serializers.DateTimeField(source='crated', read_only=True)

    class Meta:
        """Meta class."""

        model = Membership
        fields = (
            'user',
            'is_admin',
            'is_active',
            'used_invitation',
            'remaining_invitations',
            'invited_by',
            'rides_taken',
            'rides_offered',
            'joined_at'
        )
        read_only_fields = (
            'user',
            'used_invitation',
            'rides_offered',
            'rides_taken',
            'invited_by'
        )
