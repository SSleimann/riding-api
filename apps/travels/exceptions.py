from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import APIException

class RequestTravelDoesNotFound(APIException):
    status_code = 404
    default_detail = _('Request travel does not found')
    default_code = 'request_travel_error'
