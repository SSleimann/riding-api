from datetime import timedelta

from django.utils import timezone
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point

from apps.travels.models import RequestTravel
from apps.travels.services import clear_expired_request_travels

USER_MODEL = get_user_model()


class ClearExpiredRequestTravelsTestCase(TestCase):
    def setUp(self) -> None:
        self.user = USER_MODEL.objects.create_user(
            username="te122stpepe",
            email="trest21@gmail.com",
            password="testpass12345",
            first_name="test",
            last_name="test",
            is_active=True,
        )

    def test_clear_expired_request_travels(self):
        created_at = timezone.now() - timedelta(hours=1)
        origin = Point(0, 0)
        dest = Point(0, 0)

        RequestTravel.objects.create(
            user=self.user, created_time=created_at, origin=origin, destination=dest
        )
        RequestTravel.objects.create(
            user=self.user, created_time=created_at, origin=origin, destination=dest
        )
        RequestTravel.objects.create(
            user=self.user, created_time=created_at, origin=origin, destination=dest
        )
        RequestTravel.objects.create(
            user=self.user, created_time=timezone.now(), origin=origin, destination=dest
        )

        self.assertEqual(RequestTravel.objects.count(), 4)

        num_deleted = clear_expired_request_travels()

        self.assertEqual(num_deleted, 3)
        self.assertEqual(RequestTravel.objects.count(), 1)
