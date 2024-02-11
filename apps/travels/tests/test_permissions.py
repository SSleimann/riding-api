from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.exceptions import PermissionDenied

from apps.travels.permissions import IsDriverActivePermission
from apps.drivers.models import Drivers, Vehicles


class TestView(APIView):
    permission_classes = (IsDriverActivePermission,)

    def get(self, request):
        return "ok"


class IsDriverPermissionTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.view = TestView()
        self.user = get_user_model().objects.create_user(
            username="te122stpepe",
            email="trest21@gmail.com",
            password="testpass12345",
            first_name="test",
            last_name="test",
            is_active=True,
        )
        self.driver = Drivers.objects.create(user=self.user, is_active=True)
        self.request = self.factory.get("/")
        force_authenticate(self.request, user=self.user)

    def test_permission(self):
        Vehicles.objects.create(
            driver=self.driver,
            plate_number="1234",
            model="asas",
            year=1234,
            color="blue",
        )
        request = self.view.initialize_request(self.request)
        permission = self.view.check_permissions(request)
        d = Drivers.objects.get(user=self.user)

        self.assertIsNone(permission)
        self.assertTrue(d.is_active)

    def test_permissions_no_vehicles(self):
        request = self.view.initialize_request(self.request)

        with self.assertRaises(PermissionDenied):
            self.view.check_permissions(request)

        d = Drivers.objects.get(user=self.user)

        self.assertFalse(d.is_active)

    def test_permission_no_active(self):
        Vehicles.objects.create(
            driver=self.driver,
            plate_number="1234",
            model="asas",
            year=1234,
            color="blue",
        )
        request = self.view.initialize_request(self.request)

        self.driver.is_active = False
        self.driver.save()

        with self.assertRaises(PermissionDenied):
            self.view.check_permissions(request)

        d = Drivers.objects.get(user=self.user)

        self.assertFalse(d.is_active)
