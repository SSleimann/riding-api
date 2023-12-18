from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import APIException


# Model exceptions
class BaseException(Exception):
    msg: str = "Error"

    def __init__(self) -> None:
        super().__init__(self.msg)


class TooManyVehiclesException(Exception):
    msg: str = _("Maximum only two vehicles.")


# Api exceptions
class DriverDoesNotExistException(APIException):
    status_code = 404
    default_detail = _("The driver does not exists.")
    default_code = "driver_error"


class DriverDoesNotHaveVehiclesException(APIException):
    status_code = 400
    default_detail = _("The driver does not have vehicles.")
    default_code = "driver_error"


class DriverIsActiveException(APIException):
    status_code = 400
    default_detail = _("The driver is active.")
    default_code = "driver_error"


class VehicleDoesNotExistsException(APIException):
    status_code = 404
    default_detail = _("The vehicle does not exists.")
    default_code = "vehicle_error"
