from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from apps.drivers.models import Drivers
from apps.drivers.service import get_driver_by_user_id
from apps.drivers.tests.core import BaseViewTestCase

USER_MODEL = get_user_model()

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
        self.assertEqual(res.data["user"], self.user.get_full_name())
        self.assertTrue(driver)
        self.assertEqual(driver.user, self.user)
        self.assertEqual(res.data["is_active"], False)


class DriverInfoApiViewTestCase(ViewDriverTestCase):
    def test_driver_info_view(self):
        url = reverse_lazy(
            "drivers:driver_info", kwargs={"username": self.user.username}
        )

        res = self.client.get(url, headers={"Authorization": self.authorization})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["user"], self.user.get_full_name())
        self.assertEqual(res.data["is_active"], False)


class DriverMeInfoApiViewTestCase(ViewDriverTestCase):
    def test_driver_me_info_view(self):
        url = reverse_lazy("drivers:driver_me_info")

        res = self.client.get(url, headers={"Authorization": self.authorization})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["user"], self.user.get_full_name())
        self.assertEqual(res.data["is_active"], False)


class ActivateDriverApiViewTestCase(ViewDriverTestCase):
    @patch("apps.drivers.models.Drivers.has_vehicles")
    def test_activate_driver_view(self, mock_has_vehicles):
        mock_has_vehicles.return_value = True

        url = reverse_lazy("drivers:driver_activate")

        res = self.client.put(url, headers={"Authorization": self.authorization})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["user"], self.user.get_full_name())
        self.assertEqual(res.data["is_active"], True)


class InactiveDriverApiViewTestCase(ViewDriverTestCase):
    def test_inactivate_driver_view(self):
        url = reverse_lazy("drivers:driver_inactivate")

        self.driver.set_active()

        self.assertEqual(self.driver.is_active, True)

        res = self.client.put(url, headers={"Authorization": self.authorization})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["user"], self.user.get_full_name())
        self.assertEqual(res.data["is_active"], False)
