from unittest.mock import patch

from django.test import TestCase

from django.contrib.auth import get_user_model

from apps.drivers.models import Drivers, Vehicles
from apps.drivers.exceptions import TooManyVehiclesException


class VehicleManagerTestCase(TestCase):
    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
            username="test",
            password="passwdo",
            email="testemail@gmail.com",
            first_name="pablo",
            last_name="pedro",
        )

        self.driver = Drivers.objects.create(user=user)

    @patch("apps.drivers.models.VehicleManager._get_driver_vehicles_count")
    def test_error_too_many_vehicles(self, mock):
        mock.return_value = 3

        with self.assertRaises(TooManyVehiclesException):
            Vehicles.objects.create(
                driver=self.driver,
                plate_number="1234",
                model="asas",
                year=1234,
                color="blue",
            )

        self.assertTrue(mock.called)

    def test_get_driver_vehicles_count(self):
        Vehicles.objects.create(
            driver=self.driver,
            plate_number="1234",
            model="asas",
            year=1234,
            color="blue",
        )
        vehicle_count = Vehicles.objects._get_driver_vehicles_count(driver=self.driver)

        self.assertEqual(vehicle_count, 1)
