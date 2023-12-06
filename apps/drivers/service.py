from uuid import UUID

from apps.drivers.models import Drivers
from apps.drivers.exceptions import (
    DriverDoesNotHaveVehiclesException,
    DriverIsActiveException,
    DriverDoesNotExist,
)


def get_driver_by_user_id(user_id: UUID) -> Drivers:
    try:
        driver = Drivers.objects.get(user__id=user_id)
    except Drivers.DoesNotExist:
        raise DriverDoesNotExist

    return driver


def set_user_driver_active(user_id: UUID) -> Drivers:
    driver = get_driver_by_user_id(user_id)

    if not driver.is_active:
        if not driver.has_vehicles():
            raise DriverDoesNotHaveVehiclesException

        driver.set_active()

    else:
        raise DriverIsActiveException

    return driver


def set_user_driver_inactive(user_id: UUID) -> Drivers:
    driver = get_driver_by_user_id(user_id)

    if driver.is_active:
        driver.set_inactive()

    return driver
