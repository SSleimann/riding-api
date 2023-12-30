import logging

from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail

from apps.travels.models import Travel
from apps.travels.services import clear_expired_request_travels

logger = logging.getLogger(__name__)


@shared_task
def clear_expired_req_travels():
    clear_expired_request_travels()

    return "Expired requests cleared"


@shared_task(bind=True)
def send_email_to_user_by_travel(self, travel_id: int, subject: str, message: str):
    travel = Travel.objects.select_related("user").get(id=travel_id)

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [travel.user.email]

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
    except Exception as e:
        raise self.retry(exc=e, countdown=5)

    logger.info("Email sent to %s ", travel.user.email)

    return "Email sent"
