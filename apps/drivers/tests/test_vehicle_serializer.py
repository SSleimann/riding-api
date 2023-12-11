from django.utils.translation import gettext_lazy as _
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import serializers

from apps.drivers.models import Vehicles, Drivers
from apps.drivers.api.serializers.vehicle_serializer import VehiclesCreationSerializer
from apps.drivers.exceptions import TooManyVehiclesException

class VehiclesCreationSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="te122stpepe",
            email="trest21@gmail.com",
            password="testpass12345",
            first_name="test",
            last_name="test",
            is_active=True,
        )
        self.driver = Drivers.objects.create(user=self.user, is_active=True)
    
    def test_validate_serializer_vehicles_error(self):
        Vehicles.objects.create(driver=self.driver, plate_number="1234", model="asas", year=1234, color="blue")
        Vehicles.objects.create(driver=self.driver, plate_number="1234", model="asas", year=1234, color="blue")
        
        payload = dict(driver=self.driver.id, plate_number="1234", model="asas", year=1234, color="blue")
        serializer = VehiclesCreationSerializer(data=payload)
        serializer.is_valid()
        
        self.assertEqual(serializer.errors.keys(), {"vehicles"})
    
    def test_creation_serializer_vehicles_error(self):
        Vehicles.objects.create(driver=self.driver, plate_number="1234", model="asas", year=1234, color="blue")
        
        payload = dict(driver=self.driver.id, plate_number="1234", model="asas", year=1234, color="blue")
        serializer = VehiclesCreationSerializer(data=payload)
        is_valid = serializer.is_valid()
        
        Vehicles.objects.create(driver=self.driver, plate_number="1234", model="asas", year=1234, color="blue")
        
        self.assertTrue(is_valid)
        
        with self.assertRaises(serializers.ValidationError) as e:
            serializer.save()
            
        self.assertEqual(e.exception.detail.keys(), {"vehicles"})