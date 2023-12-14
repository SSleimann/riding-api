import logging

from datetime import timedelta

from django.db.models import Q
from django.utils import timezone

from apps.travels.models import RequestTravel

logger = logging.getLogger(__name__)

def clear_expired_request_travels():
    now = timezone.now()
    expired_at = now - timedelta(minutes=RequestTravel.DELETE_TIME_MIN)
    
    expired_query = Q(status=RequestTravel.PENDING) and Q(created_time__lte=expired_at)
    expired_queryset = RequestTravel.objects.filter(expired_query).values_list('id', flat=True)
    
    deleted_num, _ = RequestTravel.objects.filter(id__in=list(expired_queryset)).delete()
    
    logger.info(f"Deleted {deleted_num} expired request travels")
    
    return deleted_num
    