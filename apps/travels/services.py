import logging

from uuid import UUID

from datetime import timedelta

from django.db.models import Q
from django.utils import timezone

from apps.travels.models import RequestTravel
from apps.travels.exceptions import RequestTravelDoesNotFound

logger = logging.getLogger(__name__)


def clear_expired_request_travels():
    now = timezone.now()
    expired_at = now - timedelta(minutes=RequestTravel.DELETE_TIME_MIN)

    expired_query = Q(status=RequestTravel.PENDING) and Q(created_time__lte=expired_at)
    expired_queryset = RequestTravel.objects.filter(expired_query).values_list(
        "id", flat=True
    )

    deleted_num, _ = RequestTravel.objects.filter(
        id__in=list(expired_queryset)
    ).delete()

    logger.info(f"Deleted {deleted_num} expired request travels")

    return deleted_num

def get_request_travel_by_id(request_travel_id: int) -> RequestTravel:
    try:
        obj = RequestTravel.objects.get(id=request_travel_id)
    except RequestTravel.DoesNotExist:
        raise RequestTravelDoesNotFound
    
    return obj

def delete_request_travel_by_id_and_user_id(request_travel_id: int, user_id: UUID):
    try:
        RequestTravel.objects.get(id=request_travel_id, user__id=user_id).delete()
    except RequestTravel.DoesNotExist:
        raise RequestTravelDoesNotFound