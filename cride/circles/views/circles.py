"""Circle views."""

# Django REST Framework
from rest_framework import viewsets

# Serializers
from cride.circles.serializers import CircleModelSerializer

# Model
from cride.circles.models import Circle

class CircleViewSet(viewsets.ModelViewSet):
    """Circle view set."""

    queryset = Circle.objects.all()
    serializers_class = CircleModelSerializer
