"""User model."""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Utilities
from cride.utils.models import CRideModel


class User(CRideModel, AbstractUser):
    """User model.

    Extends from Django's AbstractUser, changing the username field
    to email and adding some extra fields.
    """

    email = models.EmailField(
        'email_address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        }
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{8,11}$',
        message="Phone number must be entered in the format  +99999999999. Up to 15 digits."
    )

    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    is_client = models.BooleanField(
        'client_status',
        default=True,
        help_text=(
            'Help easily distinguish users and performed queries. '
            'Clients are the main type of user.'
        )
    )

    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text='Sets to true when the user has verified his email address.'
    )

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.username
