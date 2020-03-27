"""Django models utilities"""

# Django
from django.db import models


class CRideModel(models.Model):
    """ComparteRide Base Model

    CRideModel acts as an actract base class from wich all other models
    will inherit.
    This class provides every table with the following attributes:
    * created (DateTime): stores DateTime object was Created
    * modified (DateTime): stores the las DateTime the object was modified.

    """

    created = models.DateTimeField(
        'create at',
        auto_now_add=True,
        help_text='Date time on which the object was created.'
    )
    modified = models.DateTimeField(
        'modifed_at',
        auto_now=True,
        help_text='Date time on which the object was last modified.'
    )

    class Meta:
        """Meta option."""
        abstract=True
        get_latest_by = 'created'
        ordering = ['-created', '-modified']
