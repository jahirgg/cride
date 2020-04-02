"""Circle views."""

# Django REST Framework
from rest_framework import mixins, viewsets

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions import IsCircleAdmin

# Serializers
from cride.circles.serializers import CircleModelSerializer

# Model
from cride.circles.models import Circle, Membership

class CircleViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """Circle view set."""

    queryset = Circle.objects.all()
    serializer_class = CircleModelSerializer
    #premission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Restrict list to public-only."""
        queryset = Circle.objects.all()
        if self.action == 'list':
            return queryset.filter(is_public=True)
        return queryset

    def get_permissions(self):
        """Assign permissions based on actions."""
        permissions = [IsAuthenticated]
        if self.action is ['update' 'partial_update']:
            permissions.append(IsCircleAdmin)
        return [permission() for permission in permissions]

    def perform_create(self, serializer):
        """Asign circle admin."""
        circle = serializer.save()
        user = self.request.user
        profile = user.profile
        Membership.objects.create(
            user=user,
            profile=profile,
            circle=circle,
            is_admin=True,
            remaining_invitations=10
        )
