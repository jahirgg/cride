"""Invitation tests."""

# Django
from django.test import TestCase

# Django REST Framework
from rest_framework import status
from rest_framework.test import APITestCase

# Models
from cride.circles.models import Circle, Invitation, Membership
from cride.users.models import User, Profile
from rest_framework.authtoken.models import Token

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


class MemberInvitationAPITestCase(APITestCase):
    """Member invitation API test cases."""

    def setUp(self):
        """Test base setup."""

        self.user = User.objects.create(
            first_name='Jahir',
            last_name='Gonzalez',
            email='jahir.gonzalez@mibus.com.pa',
            username='jahir.12130',
            password='admin123'
        )
        self.profile = Profile.objects.create(
            user=self.user
        )
        self.circle = Circle.objects.create(
            name='MiBus',
            slug_name='mibus',
            about='Grupo oficial de MiBus.',
            verified=True
        )

        self.membership = Membership.objects.create(
            user=self.user,
            profile=self.profile,
            circle=self.circle,
            remaining_invitations=10
        )

        # Auth
        self.token = Token.objects.create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token))

        # URL
        self.url = '/circles/{}/members/{}/invitations/'.format(
            self.circle.slug_name,
            self.user.username
        )

    def test_response_success(self):
        """Verify request succeeded."""
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_invitation_creation(self):
        """Verify invitations are generated if none exist previously."""
        # Invitations in db must be zero
        self.assertEqual(Invitation.objects.count(),0)

        # Call member invitations url
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

        # Verify new invitations were created
        invitations = Invitation.objects.all()
        self.assertEqual(invitations.count(),10)
        for invitation in invitations:
            self.assertIn(invitation.code, request.data['invitations'])
