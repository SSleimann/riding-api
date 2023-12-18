from datetime import timedelta

from oauth2_provider.models import get_application_model, get_access_token_model

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework.test import APIClient

USER_MODEL = get_user_model()


class BaseViewTestCase(TestCase):
    def setUp(self) -> None:
        self.user = USER_MODEL.objects.create_user(
            username="te122stpepe",
            email="trest21@gmail.com",
            password="testpass12345",
            first_name="test",
            last_name="test",
            is_active=True,
        )
        self.authorization = self.__create_authorization_header(
            self.__create_token(self.user)
        )
        self.client = APIClient()

    def __create_authorization_header(self, token):
        return "Bearer {0}".format(token)

    def __create_token(self, user):
        app_model = get_application_model()
        token_model = get_access_token_model()

        app = get_application_model().objects.create(
            client_type=app_model.CLIENT_CONFIDENTIAL,
            authorization_grant_type=app_model.GRANT_PASSWORD,
            name="dummy",
            user=user,
        )

        access_token = token_model.objects.create(
            user=user,
            scope="read write",
            expires=timezone.now() + timedelta(seconds=300),
            token="secret-access-token-key",
            application=app,
        )

        return access_token
