"""Invitation tests."""

# Django
from django.test import TestCase

# Models
from cride.circles.models import Circle, Invitation
from cride.users.models import User

class InvitationManagerTestCase(TestCase):
    """Invitation manager test case."""

    def setUp(self):
        """Test base setup."""

        self.user = User.objects.create(
            first_name='Jahir',
            last_name='Gonzalez',
            email='jahir.gonzalez@mibus.com.pa',
            username='jahir.12130',
            password='admin123'
        )

        self.circle = Circle.objects.create(
            name='MiBus',
            slug_name='mibus',
            about='Grupo oficial de MiBus.',
            verified=True
        )

    def test_code_generation(self):
        """Random codes should be generated automatically."""
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle
        )
        self.assertIsNotNone(invitation.code)

    def test_code_usage(self):
        """If a code is given there's no need to create a new one."""
        code = 'holamundo'
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
            code=code
        )
        self.assertEqual(invitation.code, code)

    def test_code_generation_if_duplicated(self):
        """If given code is not unique, a new code must be generated."""
        code = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle
        ).code

        # Create another invitation with the past code
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
            code=code
        )

        self.assertNotEqual(code, invitation.code)
