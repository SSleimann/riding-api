from datetime import timedelta

from django.urls import reverse_lazy
from django.contrib.gis.geos import Point
from django.utils import timezone

from apps.travels.tests.core import BaseViewTestCase
from apps.drivers.models import Drivers
from apps.travels.models import RequestTravel


class ViewTestCase(BaseViewTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.driver = Drivers.objects.create(user=self.user, is_active=True)


class ListRequestTravelApiViewTestCAse(ViewTestCase):
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
            created_time=timezone.now() - timedelta(hours=1),
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
            user=self.user, origin=origin, destination=destination, status=RequestTravel.TAKED
        )
        
        res = self.client.get(url,{"status": "T"}, headers={"Authorization": self.authorization})
        
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
            user=self.user, origin=origin, destination=destination, status=RequestTravel.TAKED
        )
        
        res = self.client.get(url,{"status": "P"}, headers={"Authorization": self.authorization})
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["status"], "P")