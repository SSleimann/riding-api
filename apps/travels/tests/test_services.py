from datetime import timedelta

from uuid import uuid4

from django.utils import timezone
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point

from apps.travels.models import RequestTravel
from apps.travels.services import clear_expired_request_travels, get_request_travel_by_id, delete_request_travel_by_id_and_user_id
from apps.travels.exceptions import RequestTravelDoesNotFound

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

class GetRequestTravelByIdTestCase(TestCase):
    def setUp(self) -> None:
        self.user = USER_MODEL.objects.create_user(
            username="XXXXXXXXXXX",
            email="test@gmail.com",
            password="testpass12345",
            first_name="test",
            last_name="test",
            is_active=True,
        )

    def test_get_request_travel_by_id(self):
        origin = Point(0, 0)
        dest = Point(0, 0)

        request_travel = RequestTravel.objects.create(
            user=self.user, origin=origin, destination=dest
        )

        retrieved_request_travel = get_request_travel_by_id(request_travel.id)

        self.assertEqual(retrieved_request_travel, request_travel)
    
    def test_get_request_travel_by_id_not_found(self):
        
        with self.assertRaises(RequestTravelDoesNotFound):
            get_request_travel_by_id(9000)
        
    
class DeleteRequestTravelByIdAndUserIdTestCase(TestCase):
    def setUp(self) -> None:
        self.user = USER_MODEL.objects.create_user(
            username="XXXXXXXXXXX",
            email="test@gmail.com",
            password="testpass12345",
            first_name="test",
            last_name="test",
            is_active=True,
        )
    
    def test_delete_request_travel(self):
        origin = Point(0, 0)
        dest = Point(0, 0)

        request_travel = RequestTravel.objects.create(
            user=self.user, origin=origin, destination=dest
        )
        
        delete_request_travel_by_id_and_user_id(request_travel.id, self.user.id)
        
        with self.assertRaises(RequestTravel.DoesNotExist):
            RequestTravel.objects.get(id=request_travel.id)
            
        self.assertEqual(self.user.req_travels.count(), 0)
    
    def test_delete_request_travel_not_found_rt(self):
        with self.assertRaises(RequestTravelDoesNotFound):
            delete_request_travel_by_id_and_user_id(9000, self.user.id)
    
    def test_delete_request_travel_not_found_user(self):
        origin = Point(0, 0)
        dest = Point(0, 0)
        
        request_travel = RequestTravel.objects.create(
            user=self.user, origin=origin, destination=dest
        )
        
        with self.assertRaises(RequestTravelDoesNotFound):
            delete_request_travel_by_id_and_user_id(request_travel.id, uuid4())
        