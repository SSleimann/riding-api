from uuid import UUID

from apps.drivers.models import Drivers, Vehicles
from apps.drivers.exceptions import (
    DriverDoesNotHaveVehiclesException,
    DriverIsActiveException,
    DriverDoesNotExistException,
    VehicleDoesNotExistsException,
)


def get_driver_by_user_id(user_id: UUID) -> Drivers:
    try:
        driver = Drivers.objects.get(user__id=user_id)
    except Drivers.DoesNotExist:
        raise DriverDoesNotExistException

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


def delete_vehicle_by_id_and_driver_id(vehicle_id: UUID, driver_id: UUID) -> None:
    try:
        Vehicles.objects.get(id=vehicle_id, driver__id=driver_id).delete()
    except Vehicles.DoesNotExist:
        raise VehicleDoesNotExistsException


def get_vehicle_by_id(vehicle_id: UUID) -> Vehicles:
    try:
        vehicle = Vehicles.objects.select_related("driver").get(id=vehicle_id)
    except Vehicles.DoesNotExist:
        raise VehicleDoesNotExistsException

    return vehicle
