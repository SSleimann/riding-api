from unittest.mock import patch

from uuid import uuid4

from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.drivers.models import Drivers, Vehicles
from apps.drivers.service import (
    set_user_driver_active,
    set_user_driver_inactive,
    get_driver_by_user_id,
    delete_vehicle_by_id_and_driver_id,
    get_vehicle_by_id,
)
from apps.drivers.exceptions import (
    DriverDoesNotExistException,
    DriverDoesNotHaveVehiclesException,
    DriverIsActiveException,
    VehicleDoesNotExistsException,
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
        with self.assertRaises(DriverDoesNotExistException):
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

        self.assertTrue(mock_has_vehicles.called)
        self.assertTrue(driver.is_active)

    def test_driver_doesnt_exist(self):
        with self.assertRaises(DriverDoesNotExistException):
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

        self.assertTrue(mock_has_vehicles.called)
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
        with self.assertRaises(DriverDoesNotExistException):
            set_user_driver_inactive(uuid4())

        self.assertTrue(self.driver.is_active)


class DeleteVehicleByIdAndDriverIdTestCase(TestCase):
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
        self.vehicle = Vehicles.objects.create(
            driver=self.driver,
            plate_number="1234",
            model="asas",
            year=1234,
            color="blue",
        )

    def test_delete_vehicle(self):
        vehicle_id = self.vehicle.id

        self.assertTrue(
            Vehicles.objects.filter(id=vehicle_id, driver__id=self.driver.id).exists()
        )

        delete_vehicle_by_id_and_driver_id(vehicle_id, self.driver.id)

        self.assertFalse(Vehicles.objects.filter(id=vehicle_id).exists())
        self.assertFalse(
            Vehicles.objects.filter(id=vehicle_id, driver__id=self.driver.id).exists()
        )

    def test_delete_vehicle_does_not_exist(self):
        with self.assertRaises(VehicleDoesNotExistsException):
            delete_vehicle_by_id_and_driver_id(uuid4(), self.driver.id)

    def test_delete_vehicle_with_invalid_driver(self):
        with self.assertRaises(VehicleDoesNotExistsException):
            delete_vehicle_by_id_and_driver_id(self.vehicle.id, uuid4())


class GetVehicleByIdTestCase(TestCase):
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
        self.vehicle = Vehicles.objects.create(
            driver=self.driver,
            plate_number="1234",
            model="asas",
            year=1234,
            color="blue",
        )

    def test_get_vehicle_by_id(self):
        vehicle = get_vehicle_by_id(self.vehicle.id)

        self.assertEqual(vehicle.id, self.vehicle.id)
        self.assertEqual(vehicle.driver.id, self.driver.id)
        self.assertEqual(vehicle.plate_number, self.vehicle.plate_number)
        self.assertEqual(vehicle.model, self.vehicle.model)
        self.assertEqual(vehicle.year, self.vehicle.year)
        self.assertEqual(vehicle.color, self.vehicle.color)

    def test_get_vehicle_does_not_exist(self):
        with self.assertRaises(VehicleDoesNotExistsException):
            get_vehicle_by_id(uuid4())
