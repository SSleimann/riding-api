from datetime import timedelta

from unittest.mock import patch

from oauth2_provider.models import get_application_model, get_access_token_model

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils import timezone

from rest_framework.test import APIClient

from apps.drivers.models import Drivers
from apps.drivers.service import get_driver_by_user_id

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
        self.authorization = self.__create_authorization_header(self.__create_token(self.user))
        self.client = APIClient()
    
    def __create_authorization_header(self, token):
        return "Bearer {0}".format(token)

    def __create_token(self, user):
        app_model = get_application_model()
        token_model = get_access_token_model()
        
        app = get_application_model().objects.create(
            client_type=app_model.CLIENT_CONFIDENTIAL,
            authorization_grant_type=app_model.GRANT_PASSWORD,
            name='dummy',
            user=user
        )
        
        access_token = token_model.objects.create(
            user=user,
            scope='read write',
            expires=timezone.now() + timedelta(seconds=300),
            token='secret-access-token-key',
            application=app
        )
        
        return access_token
        
class ViewDriverTestCase(BaseViewTestCase):
    def setUp(self) -> None:
        super().setUp()
        
        self.driver = Drivers.objects.create(user=self.user)

class CreateDriverApiViewTestCase(BaseViewTestCase):
    def test_create_driver_view(self):
        url = reverse_lazy("drivers:driver_create")
        
        res = self.client.post(url, headers={"Authorization": self.authorization})
        
        driver = get_driver_by_user_id(self.user.id)
        
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data["user"], self.user.username)
        self.assertTrue(driver)
        self.assertEqual(driver.user, self.user)
        self.assertEqual(res.data["is_active"], False)
    
class DriverInfoApiViewTestCase(ViewDriverTestCase):
    def test_driver_info_view(self):
        url = reverse_lazy("drivers:driver_info", kwargs={"username": self.user.username})
        
        res = self.client.get(url, headers={"Authorization": self.authorization})
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["user"], self.user.username)
        self.assertEqual(res.data["is_active"], False)
    
class DriverMeInfoApiViewTestCase(ViewDriverTestCase):
    def test_driver_me_info_view(self):
        url = reverse_lazy("drivers:driver_me_info")
        
        res = self.client.get(url, headers={"Authorization": self.authorization})
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["user"], self.user.username)
        self.assertEqual(res.data["is_active"], False)
    
class ActivateDriverApiViewTestCase(ViewDriverTestCase):
    
    @patch("apps.drivers.models.Drivers.has_vehicles")
    def test_activate_driver_view(self, mock_has_vehicles):
        mock_has_vehicles.return_value = True
        
        url = reverse_lazy("drivers:driver_activate")
        
        res = self.client.put(url, headers={"Authorization": self.authorization})
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["user"], self.user.username)
        self.assertEqual(res.data["is_active"], True)
    
class InactiveDriverApiViewTestCase(ViewDriverTestCase):
    def test_inactivate_driver_view(self):
        url = reverse_lazy("drivers:driver_inactivate")
        
        self.driver.set_active()
        
        self.assertEqual(self.driver.is_active, True)
        
        res = self.client.put(url, headers={"Authorization": self.authorization})
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["user"], self.user.username)
        self.assertEqual(res.data["is_active"], False)