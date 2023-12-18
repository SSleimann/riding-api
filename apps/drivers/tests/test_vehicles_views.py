from uuid import uuid4

from django.urls import reverse_lazy

from apps.drivers.models import Drivers, Vehicles
from apps.drivers.tests.core import BaseViewTestCase
from apps.drivers.exceptions import VehicleDoesNotExistsException


class ViewVehicleTestCase(BaseViewTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.driver = Drivers.objects.create(user=self.user)
        self.vehicle = Vehicles.objects.create(
            driver=self.driver,
            plate_number="1234",
            model="asas",
            year=1234,
            color="blue",
        )


class VehiclesCreationApiViewTestCase(ViewVehicleTestCase):
    def test_create_vehicle(self):
        url = reverse_lazy("drivers:vehicles_create")

        payload = {
            "plate_number": "1234",
            "model": "asas",
            "year": 1234,
            "color": "blue",
        }
        response = self.client.post(
            url, payload, headers={"Authorization": self.authorization}
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Vehicles.objects.get(id=response.data["id"]))
        self.assertEqual(response.data["plate_number"], "1234")
        self.assertEqual(response.data["model"], "asas")
        self.assertEqual(response.data["year"], 1234)
        self.assertEqual(response.data["color"], "blue")
        self.assertEqual(response.data["driver"], self.driver.driver_name)

    def test_create_vehicle_error_vehicles(self):
        Vehicles.objects.create(
            driver=self.driver,
            plate_number="1234",
            model="asas",
            year=1234,
            color="blue",
        )

        url = reverse_lazy("drivers:vehicles_create")

        payload = {
            "plate_number": "1234",
            "model": "asas",
            "year": 1234,
            "color": "blue",
        }
        response = self.client.post(
            url, payload, headers={"Authorization": self.authorization}
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("vehicles", response.data)


class VehiclesDetailApiViewTestCase(ViewVehicleTestCase):
    def test_get_vehicle(self):
        url = reverse_lazy("drivers:vehicles_detail", kwargs={"uuid": self.vehicle.id})
        response = self.client.get(url, headers={"Authorization": self.authorization})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["plate_number"], self.vehicle.plate_number)
        self.assertEqual(response.data["model"], self.vehicle.model)
        self.assertEqual(response.data["year"], self.vehicle.year)
        self.assertEqual(response.data["color"], self.vehicle.color)
        self.assertEqual(response.data["driver"], self.driver.driver_name)

    def test_get_vehicle_not_found(self):
        url = reverse_lazy(
            "drivers:vehicles_detail", kwargs={"uuid": uuid4().__str__()}
        )
        response = self.client.get(url, headers={"Authorization": self.authorization})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data["detail"], VehicleDoesNotExistsException.default_detail
        )


class VehiclesListApiViewTestCase(ViewVehicleTestCase):
    def test_get_list_vehicles(self):
        Vehicles.objects.create(
            driver=self.driver,
            plate_number="1234",
            model="asas",
            year=1234,
            color="blue",
        )

        url = reverse_lazy("drivers:vehicles_list")

        response = self.client.get(url, headers={"Authorization": self.authorization})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)


class VehiclesDeleteApiViewApiView(ViewVehicleTestCase):
    def test_delete_vehicles(self):
        url = reverse_lazy("drivers:vehicles_delete", kwargs={"uuid": self.vehicle.id})

        response = self.client.delete(
            url, headers={"Authorization": self.authorization}
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Vehicles.objects.filter(id=self.vehicle.id).exists())

    def test_delete_vehicle_not_found(self):
        url = reverse_lazy(
            "drivers:vehicles_delete", kwargs={"uuid": uuid4().__str__()}
        )

        response = self.client.delete(
            url, headers={"Authorization": self.authorization}
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data["detail"], VehicleDoesNotExistsException.default_detail
        )
