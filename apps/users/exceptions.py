from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import APIException


class UserNotFound(APIException):
    status_code = 404
    default_detail = _("User not found")
    default_code = "user_error"
