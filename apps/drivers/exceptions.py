from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import APIException

class DriverDoesNotExist(APIException):
    status_code = 400
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
