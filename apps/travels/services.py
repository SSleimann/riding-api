import logging

from uuid import UUID

from django.db.models import Q
from django.utils import timezone
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db import transaction, DatabaseError

from apps.travels.models import RequestTravel, Travel, ConfirmationTravel
from apps.travels.exceptions import (
    RequestTravelDoesNotFound,
    DriverCantTakeRequestTravel,
    TravelDoesNotFound,
    CannotCancelThisTravel,
    CannotFinishThisTravel,
    InvalidVehicleDriver,
)
from apps.drivers.service import get_driver_by_user_id, get_vehicle_by_id
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


def take_request_travel(
    request_travel_id: int, user_id: UUID, long: float, lat: float, vehicle_id: UUID
):
    driver_loc = Point(long, lat)
    driver = get_driver_by_user_id(user_id)
    vehicle = get_vehicle_by_id(vehicle_id)

    if vehicle.driver != driver:
        raise InvalidVehicleDriver

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
                vehicle=vehicle,
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


def finish_travel(travel_id: int, user_id: UUID) -> ConfirmationTravel:
    travel = get_travel_by_id(travel_id)
    user_finisher = get_user_by_id(user_id)

    if travel.status != Travel.IN_COURSE:
        raise CannotFinishThisTravel

    confirmation_travel, _ = ConfirmationTravel.objects.get_or_create(travel=travel)

    try:
        if user_finisher.id == travel.user.id:
            confirmation_travel.user = user_finisher
        elif travel.driver.id == user_finisher.drivers.id:
            confirmation_travel.driver = user_finisher.drivers
        else:
            raise CannotFinishThisTravel

        confirmation_travel.save()

    except User.drivers.RelatedObjectDoesNotExist:
        raise CannotFinishThisTravel

    if confirmation_travel.user is not None and confirmation_travel.driver is not None:
        travel.status = Travel.DONE
        travel.save()

    return confirmation_travel
