import logging

from uuid import UUID

from django.db.models import Q
from django.utils import timezone
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db import transaction, DatabaseError

from apps.travels.models import RequestTravel, Travel
from apps.travels.exceptions import (
    RequestTravelDoesNotFound,
    DriverCantTakeRequestTravel,
    TravelDoesNotFound,
    CannotCancelThisTravel,
)
from apps.drivers.service import get_driver_by_user_id
from apps.users.services import get_user_by_id
from apps.users.models import User

logger = logging.getLogger(__name__)


def clear_expired_request_travels():
    expired_query = Q(status=RequestTravel.PENDING) and Q(expires__lte=timezone.now())
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


def take_request_travel(request_travel_id: int, user_id: UUID, long: float, lat: float):
    driver_loc = Point(long, lat)
    driver = get_driver_by_user_id(user_id)

    try:
        request_travel = RequestTravel.objects.select_related("user").get(
            status=RequestTravel.PENDING,
            id=request_travel_id,
            expires__gte=timezone.now(),
            origin__distance_lte=(driver_loc, D(km=RequestTravel.MAX_RADIUS)),
        )
    except RequestTravel.DoesNotExist:
        raise RequestTravelDoesNotFound

    if driver.user.id == request_travel.user.id:
        raise DriverCantTakeRequestTravel

    try:
        with transaction.atomic():
            request_travel.status = RequestTravel.TAKED
            request_travel.save()

            travel = Travel.objects.create(
                user=request_travel.user,
                driver=driver,
                request_travel=request_travel,
                origin=request_travel.origin,
                destination=request_travel.destination,
            )

    except DatabaseError as e:
        logger.exception("DATABASE ERROR: %s", e, exc_info=True)
        raise DriverCantTakeRequestTravel

    return travel


def get_travel_by_id(travel_id: int) -> Travel:
    try:
        travel = Travel.objects.get(id=travel_id)
    except Travel.DoesNotExist:
        raise TravelDoesNotFound

    return travel


def cancel_travel(travel_id: int, user_id: UUID) -> Travel:
    def validation_for_cancel(travel: Travel, user: User) -> bool:
        if travel.status != Travel.IN_COURSE:
            return False

        try:
            if (travel.user.id == user.id) or (travel.driver.id == user.drivers.id):
                return True
        except User.drivers.RelatedObjectDoesNotExist:
            return False

        return False

    travel = get_travel_by_id(travel_id)
    user_deleter = get_user_by_id(user_id)

    if not validation_for_cancel(travel, user_deleter):
        raise CannotCancelThisTravel

    travel.status = Travel.CANCELLED
    travel.save()

    return travel
