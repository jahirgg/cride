"""Users serializers."""

# Django
from django.conf import settings
from django.contrib.auth import password_validation, authenticate
from django.core.validators import RegexValidator

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Serializers
from cride.users.serializers.profile import ProfileModelSerializer

# Models
from cride.users.models import User, Profile

# Celery
from cride.taskapp.tasks import send_confirmation_email

# JWT
import jwt


class UserModelSerializer(serializers.ModelSerializer):
    """User Model serializer"""

    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        """Meta Class"""
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'profile'
        )


class UserSignUpSerializer(serializers.Serializer):
    """User Sign Up Serializer.

    Hangle sign up data user validation and user and profile creation
    """

    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{8,11}$',
        message="Phone number must be entered in the format  +99999999999. Up to 15 digits."
    )

    phone_number = serializers.CharField(
        validators=[phone_regex]
    )

    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    first_name = serializers.CharField(
        min_length=2,
        max_length=30
    )

    last_name = serializers.CharField(
        min_length=2,
        max_length=30
    )

    def validate(self, data):
        """Verify passwords match"""
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError('Passwords do not match.')
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        """Handle user and profile creation."""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_verified=False, is_client=True)
        Profile.objects.create(user=user)
        send_confirmation_email.delay(user_pk=user.pk)
        return user


class UserLoginSerializer(serializers.Serializer):
    """User login serializer.

    Hangle the login request data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Verify credentials."""
        user = authenticate(
            username=data['email'],
            password=data['password']
        )
        if not user:
            raise serializers.ValidationError('Invalid credentials.')
        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet.')
        self.context['user'] = user
        return data

    def create(self, data):
        """Generate or retrieve new token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer."""
    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid"""
        try:
            payload = jwt.decode(
                data,
                settings.SECRET_KEY,
                algorithm=['HS256']
            )
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expiered')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid Token')
        if payload['type'] is 'email_confiramtion':
            raise serializers.ValidationError('Invalid Token')

        self.context['payload'] = payload
        return data

    def save(self):
        """Updates user's verified status"""
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()
