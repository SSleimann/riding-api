from django.urls import reverse_lazy
from django.contrib.gis.geos import Point
from django.contrib.auth import get_user_model
from django.core import mail

from apps.travels.tests.core import BaseViewTestCase
from apps.drivers.models import Drivers
from apps.travels.models import RequestTravel, Travel
from apps.travels.exceptions import (
    DriverCantTakeRequestTravel,
    TravelDoesNotFound,
    CannotCancelThisTravel,
)

from riding.celery import app


class ViewTestCase(BaseViewTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.driver = Drivers.objects.create(user=self.user, is_active=True)

        self.user2 = get_user_model().objects.create_user(
            username="te1212stpepe",
            email="trest2111@gmail.com",
            password="testpass12345",
            first_name="test",
            last_name="test",
            is_active=True,
        )


class TakeRequestTravelApiViewTestCase(ViewTestCase):
    def setUp(self) -> None:
        super().setUp()

        app.conf.update(CELERY_TASK_ALWAYS_EAGER=True)

    def test_take_request_travel_api_view(self):
        request_travel = RequestTravel.objects.create(
            user=self.user2, origin=Point(0, 0), destination=Point(0, 0)
        )

        url = reverse_lazy(
            "travels:travel_take_request_travel",
            kwargs={"request_travel_id": request_travel.id},
        )
        payload = {"longitude": 0, "latitude": 0}

        res = self.client.post(
            path=url,
            data=payload,
            headers={"Authorization": self.authorization},
        )

        travel = Travel.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, 200)
        self.assertEqual(travel.user, self.user2)
        self.assertEqual(travel.driver, self.driver)
        self.assertEqual(travel.request_travel.id, request_travel.id)
        self.assertEqual(travel.request_travel.status, RequestTravel.TAKED)
        self.assertEqual(Travel.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Your travel request has been taken!")
        self.assertEqual(mail.outbox[0].to, [self.user2.email])

    def test_take_request_travel_self(self):
        request_travel = RequestTravel.objects.create(
            user=self.user, origin=Point(0, 0), destination=Point(0, 0)
        )

        url = reverse_lazy(
            "travels:travel_take_request_travel",
            kwargs={"request_travel_id": request_travel.id},
        )
        payload = {"longitude": 0, "latitude": 0}

        res = self.client.post(
            path=url,
            data=payload,
            headers={"Authorization": self.authorization},
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(res.data["detail"], DriverCantTakeRequestTravel.default_detail)


class TravelApiViewTestCase(ViewTestCase):
    def test_travel_api_view(self):
        request_travel = RequestTravel.objects.create(
            user=self.user2, origin=Point(0, 0), destination=Point(0, 0)
        )
        travel = Travel.objects.create(
            user=request_travel.user,
            driver=self.driver,
            request_travel=request_travel,
            origin=request_travel.origin,
            destination=request_travel.destination,
        )

        url = reverse_lazy("travels:travel_retrieve", kwargs={"travel_id": travel.id})

        res = self.client.get(
            path=url,
            headers={"Authorization": self.authorization},
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["id"], travel.id)
        self.assertEqual(res.data["user"], request_travel.user.id)
        self.assertEqual(res.data["driver"], self.driver.id)
        self.assertEqual(res.data["request_travel"], request_travel.id)

    def test_travel_api_view_not_found(self):
        url = reverse_lazy("travels:travel_retrieve", kwargs={"travel_id": 1})

        res = self.client.get(
            path=url,
            headers={"Authorization": self.authorization},
        )

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.data["detail"], TravelDoesNotFound.default_detail)


class CancelTravelApiView(ViewTestCase):
    def setUp(self) -> None:
        super().setUp()

        app.conf.update(CELERY_TASK_ALWAYS_EAGER=True)

    def test_cancel_travel_api_view(self):
        request_travel = RequestTravel.objects.create(
            user=self.user2, origin=Point(0, 0), destination=Point(0, 0)
        )
        travel = Travel.objects.create(
            user=request_travel.user,
            driver=self.driver,
            request_travel=request_travel,
            origin=request_travel.origin,
            destination=request_travel.destination,
        )

        url = reverse_lazy("travels:travel_cancel", kwargs={"travel_id": travel.id})

        res = self.client.post(
            path=url,
            headers={"Authorization": self.authorization},
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["id"], travel.id)
        self.assertEqual(res.data["user"], travel.user.id)
        self.assertEqual(res.data["driver"], travel.driver.id)
        self.assertEqual(res.data["status"], Travel.CANCELLED)
        self.assertEqual(Travel.objects.get(id=travel.id).status, Travel.CANCELLED)
        self.assertEqual(len(mail.outbox), 1)

    def test_cancel_travel_api_view_not_found(self):
        url = reverse_lazy("travels:travel_cancel", kwargs={"travel_id": 1})

        res = self.client.post(
            path=url,
            headers={"Authorization": self.authorization},
        )

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.data["detail"], TravelDoesNotFound.default_detail)
        self.assertEqual(len(mail.outbox), 0)

    def test_cancel_travel_api_view_not_user(self):
        driver2 = Drivers.objects.create(user=self.user2)

        request_travel = RequestTravel.objects.create(
            user=self.user2, origin=Point(0, 0), destination=Point(0, 0)
        )

        travel = Travel.objects.create(
            user=request_travel.user,
            driver=driver2,
            request_travel=request_travel,
            origin=request_travel.origin,
            destination=request_travel.destination,
        )

        url = reverse_lazy("travels:travel_cancel", kwargs={"travel_id": travel.id})

        res = self.client.post(
            path=url,
            headers={"Authorization": self.authorization},
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data["detail"], CannotCancelThisTravel.default_detail)
        self.assertEqual(len(mail.outbox), 0)
