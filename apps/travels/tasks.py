from celery import shared_task

from apps.travels.services import clear_expired_request_travels


@shared_task
def clear_expired_req_travels():
    clear_expired_request_travels()

    return "Expired requests cleared"
