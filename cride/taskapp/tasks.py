"""Celery Tasks."""

# Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# Models
from cride.users.models import User
from cride.rides.models import Ride

# Utilities
from datetime import timedelta

# JWT
import jwt
import time

# Celery
from celery.decorators import task, periodic_task


@task(name='send_confirmation_email', max_retries=3)
def send_confirmation_email(user_pk):
    """Send account verification link to given user."""
    for i in range(30):
        time.sleep(1)
        print("Sleeping ", str(i+1))
    user = User.objects.get(pk=user_pk)
    verification_token = gen_verification_token(user)

    subject = 'Welcome @{}! Verify your account to start using Comparte Ride.'.format(user.first_name)
    from_email = 'Comparte Ride <noreply@comparteride.com>'
    content = render_to_string(
        'emails/users/account_verification.html',
        {'token': verification_token, 'user': user}
    )
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, "text/html")
    msg.send()

    print('Sending email')


def gen_verification_token(user):
    """Create JWT token that the user can use to verify his account."""
    exp_date = timezone.now() + timedelta(days=3)
    payload = {
        'user': user.username,
        'exp': int(exp_date.timestamp()),
        'type': 'email_confirmation'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, 'HS256')

    return token.decode()


@periodic_task(name='disable_finished_rides', run_every=timedelta(minutes=30))
def disable_finished_rides():
    """Disable finished rides."""
    now = timezone.now()
    offset = now + timedelta(minutes=30)

    # Update rides that have alreday finished
    rides = Ride.objects.filter(arrival_date__gte=now,
                                arrival_date__lte=offset,
                                is_active=True
                                )
    rides.update(is_active=False)
