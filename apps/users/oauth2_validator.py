from oauth2_provider.oauth2_validators import OAuth2Validator

from django.contrib.auth import authenticate
from django.http import HttpRequest


class CustomOAuth2Validator(OAuth2Validator):
    def validate_user(self, username, password, client, request, *args, **kwargs):
        http_request = HttpRequest()
        http_request.path = request.uri
        http_request.method = request.http_method

        getattr(http_request, request.http_method).update(dict(request.decoded_body))

        http_request.META = request.headers

        u = authenticate(http_request, username=username, password=password)

        if u is not None and u.is_active and u.is_verified:
            request.user = u
            return True

        return False
