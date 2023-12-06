from unittest.mock import patch

from uuid import uuid4

from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.drivers.models import Drivers
from apps.drivers.service import (
    set_user_driver_active,
    set_user_driver_inactive,
    get_driver_by_user_id,
)
from apps.drivers.exceptions import (
    DriverDoesNotExist,
    DriverDoesNotHaveVehiclesException,
    DriverIsActiveException,
)

USER_MODEL = get_user_model()


class GetDriverByUserIdServiceTestCase(TestCase):
    def setUp(self) -> None:
        self.user = USER_MODEL.objects.create_user(
            username="te122stpepe",
            email="trest21@gmail.com",
            password="testpass12345",
            first_name="test",
            last_name="test",
            is_active=True,
        )
        self.driver = Drivers.objects.create(user=self.user, is_active=True)

    def test_get_driver_by_userid(self):
        driver = get_driver_by_user_id(self.user.id)

        self.assertTrue(driver)
        self.assertEqual(driver.id, self.driver.id)

    def test_driver_doesnt_exist(self):
        with self.assertRaises(DriverDoesNotExist):
            get_driver_by_user_id(uuid4())


class SetUserDriverActiveServiceTestCase(TestCase):
    def setUp(self) -> None:
        self.user = USER_MODEL.objects.create_user(
            username="te122stpepe",
            email="trest21@gmail.com",
            password="testpass12345",
            first_name="test",
            last_name="test",
            is_active=True,
        )

        self.driver = Drivers.objects.create(user=self.user, is_active=False)

    @patch("apps.drivers.models.Drivers.has_vehicles")
    def test_activate_user(self, mock_has_vehicles):
        mock_has_vehicles.return_value = True

        driver = set_user_driver_active(self.user.id)

        self.assertTrue(driver.is_active)

    def test_driver_doesnt_exist(self):
        with self.assertRaises(DriverDoesNotExist):
            set_user_driver_active(uuid4())

        self.assertFalse(self.driver.is_active)

    def test_driver_is_active(self):
        self.driver.is_active = True
        self.driver.save()

        with self.assertRaises(DriverIsActiveException):
            set_user_driver_active(self.user.id)

        self.assertTrue(self.driver.is_active)

    @patch("apps.drivers.models.Drivers.has_vehicles")
    def test_driver_has_not_vehicles(self, mock_has_vehicles):
        mock_has_vehicles.return_value = False

        with self.assertRaises(DriverDoesNotHaveVehiclesException):
            set_user_driver_active(self.user.id)

        self.assertFalse(self.driver.is_active)


class SetUserDriverInactiveTestCase(TestCase):
    def setUp(self):
        self.user = USER_MODEL.objects.create_user(
            username="te122stpepe",
            email="trest21@gmail.com",
            password="testpass12345",
            first_name="test",
            last_name="test",
            is_active=True,
        )
        self.driver = Drivers.objects.create(user=self.user, is_active=True)

    def test_inactivate_driver(self):
        driver = set_user_driver_inactive(self.user.id)

        self.assertFalse(driver.is_active)

    def test_driver_doesnt_exist(self):
        with self.assertRaises(DriverDoesNotExist):
            set_user_driver_inactive(uuid4())

        self.assertTrue(self.driver.is_active)
