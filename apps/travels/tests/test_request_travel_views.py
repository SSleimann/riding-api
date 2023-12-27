from datetime import timedelta

from django.urls import reverse_lazy
from django.contrib.gis.geos import Point
from django.utils import timezone
from django.contrib.auth import get_user_model

from apps.travels.tests.core import BaseViewTestCase
from apps.drivers.models import Drivers
from apps.travels.models import RequestTravel
from apps.travels.exceptions import RequestTravelDoesNotFound

class ViewTestCase(BaseViewTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.driver = Drivers.objects.create(user=self.user, is_active=True)


class ListRequestTravelApiViewTestCase(ViewTestCase):
    def test_get_list_request_travels(self):
        origin = Point(0, 0)
        destination = Point(0, 0)
        
        RequestTravel.objects.create(
            user=self.user, origin=origin, destination=destination
        )
        RequestTravel.objects.create(
            user=self.user, origin=origin, destination=destination
        )
        RequestTravel.objects.create(
            user=self.user,
            origin=origin,
            destination=destination,
            expires=timezone.now() - timedelta(hours=1),
        )

        url = reverse_lazy("travels:request_travel_list")

        res = self.client.get(
            url,
            {"latitude": 0, "longitude": 0},
            headers={"Authorization": self.authorization},
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 2)

    def test_get_list_not_active_driver(self):
        self.driver.is_active = False
        self.driver.save()

        url = reverse_lazy("travels:request_travel_list")

        res = self.client.get(
            url,
            {"latitude": 0, "longitude": 0},
            headers={"Authorization": self.authorization},
        )

        self.assertEqual(res.data["detail"].code, "permission_denied")
        self.assertEqual(res.status_code, 403)

    def test_get_list_not_driver_exist(self):
        self.driver.delete()

        url = reverse_lazy("travels:request_travel_list")

        res = self.client.get(
            url,
            {"latitude": 0, "longitude": 0},
            headers={"Authorization": self.authorization},
        )

        self.assertEqual(res.data["detail"].code, "permission_denied")
        self.assertEqual(res.status_code, 403)


class ListRequestTravelUserApiViewTestCase(ViewTestCase):
    def test_list_rt_user(self):
        url = reverse_lazy("travels:request_travel_user_list")

        origin = Point(0, 0)
        destination = Point(0, 0)

        RequestTravel.objects.create(
            user=self.user, origin=origin, destination=destination
        )

        RequestTravel.objects.create(
            user=self.user, origin=origin, destination=destination
        )

        res = self.client.get(url, headers={"Authorization": self.authorization})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 2)

    def test_list_rt_user_query_taked(self):
        url = reverse_lazy("travels:request_travel_user_list")

        origin = Point(0, 0)
        destination = Point(0, 0)

        RequestTravel.objects.create(
            user=self.user, origin=origin, destination=destination
        )

        RequestTravel.objects.create(
            user=self.user,
            origin=origin,
            destination=destination,
            status=RequestTravel.TAKED,
        )

        res = self.client.get(
            url, {"status": "T"}, headers={"Authorization": self.authorization}
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["status"], "T")

    def test_list_rt_user_query_pending(self):
        url = reverse_lazy("travels:request_travel_user_list")

        origin = Point(0, 0)
        destination = Point(0, 0)

        RequestTravel.objects.create(
            user=self.user, origin=origin, destination=destination
        )

        RequestTravel.objects.create(
            user=self.user,
            origin=origin,
            destination=destination,
            status=RequestTravel.TAKED,
        )

        res = self.client.get(
            url, {"status": "P"}, headers={"Authorization": self.authorization}
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["status"], "P")


class CreateRequestTravelApiViewTestCase(ViewTestCase):
    def test_create_rt(self):
        url = reverse_lazy("travels:request_travel_create")

        payload = {
            "destination": {"type": "Point", "coordinates": [0, 0]},
            "origin": {"type": "Point", "coordinates": [0, 0]},
        }

        res = self.client.post(
            url,
            data=payload,
            headers={"Authorization": self.authorization},
            format="json",
        )

        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data["status"], "P")
        self.assertEqual(res.data["user"], self.user.id)
        self.assertEqual(res.data["id"], RequestTravel.objects.first().id)

class RequestTravelApiViewTestCase(ViewTestCase):
    def test_get_rt(self):
        origin = Point(0, 0)
        destination = Point(0, 0)

        rt =RequestTravel.objects.create(
            user=self.user, origin=origin, destination=destination
        )
        
        url = reverse_lazy("travels:request_travel_get_delete", kwargs={"id": rt.id})
        
        res = self.client.get(url, headers={"Authorization": self.authorization})
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["id"], rt.id)
        self.assertEqual(res.data["user"], self.user.id)
        self.assertEqual(res.data["status"], "P")
        
    def test_delete_rt(self):
        origin = Point(0, 0)
        destination = Point(0, 0)

        rt =RequestTravel.objects.create(
            user=self.user, origin=origin, destination=destination
        )
        
        url = reverse_lazy("travels:request_travel_get_delete", kwargs={"id": rt.id})
        
        res = self.client.delete(url, headers={"Authorization": self.authorization})
        
        self.assertEqual(res.status_code, 204)
        self.assertEqual(RequestTravel.objects.count(), 0)
    
    def test_delete_rt_not_exist(self):
        url = reverse_lazy("travels:request_travel_get_delete", kwargs={"id": 1})
        
        res = self.client.delete(url, headers={"Authorization": self.authorization})
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.data["detail"], RequestTravelDoesNotFound.default_detail)
    
    def test_get_rt_not_exist(self):
        url = reverse_lazy("travels:request_travel_get_delete", kwargs={"id": 1})
        
        res = self.client.get(url, headers={"Authorization": self.authorization})
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.data["detail"], RequestTravelDoesNotFound.default_detail)
    
    def test_delete_rt_owner_permission(self):
        origin = Point(0, 0)
        destination = Point(0, 0)
        
        user2 = get_user_model().objects.create_user(
            username="te1212stpepe",
            email="trest2111@gmail.com",
            password="testpass12345",
            first_name="test",
            last_name="test",
            is_active=True,
        )
        
        rt =RequestTravel.objects.create(
            user=user2, origin=origin, destination=destination
        )
        
        url = reverse_lazy("travels:request_travel_get_delete", kwargs={"id": rt.id})
        
        res = self.client.delete(url, headers={"Authorization": self.authorization})
        
        self.assertEqual(res.status_code, 403)