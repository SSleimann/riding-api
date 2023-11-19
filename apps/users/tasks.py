import logging

from datetime import timedelta

from celery import shared_task

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from apps.users.security import create_jwt_token

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def send_verification_email(self, user_pk):
    user = get_user_model().objects.get(pk=user_pk)
    payload = {"user_username": user.username, "type": "_email_confirmation"}

    verify_token = create_jwt_token(payload, settings.JWT_SECRET_KEY, timedelta(days=1))

    subject = "Email Verification!"
    from_email = settings.EMAIL_HOST_USER
    message = """
    Hello, {0}

    If you want to use the API you must verify your account.

    To do that make a POST request in {1} with this token:

    {2}
    """.format(
        user.username, reverse_lazy("users:user_verify"), verify_token
    )

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[user.email],
        )
    except Exception as e:
        raise self.retry(exc=e, countdown=5)

    logger.info("Email sent to {}".format(user.email))

    return "Email Sent"
