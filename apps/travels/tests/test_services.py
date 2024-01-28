from datetime import timedelta

from uuid import uuid4

from django.utils import timezone
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point

from apps.travels.models import RequestTravel, Travel, ConfirmationTravel
from apps.travels.services import (
    clear_expired_request_travels,
    get_request_travel_by_id,
    delete_request_travel_by_id_and_user_id,
    take_request_travel,
    get_travel_by_id,
    cancel_travel,
    finish_travel,
)
from apps.travels.exceptions import (
    RequestTravelDoesNotFound,
    DriverCantTakeRequestTravel,
    TravelDoesNotFound,
    CannotCancelThisTravel,
    CannotFinishThisTravel,
    InvalidVehicleDriver,
)
from apps.drivers.models import Drivers, Vehicles
from apps.users.exceptions import UserNotFound

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
        origin = Point(0, 0)
        dest = Point(0, 0)

        expires = timezone.now() - timedelta(hours=2)

        RequestTravel.objects.create(
            user=self.user, origin=origin, destination=dest, expires=expires
        )
        RequestTravel.objects.create(
            user=self.user, origin=origin, destination=dest, expires=expires
        )
        RequestTravel.objects.create(
            user=self.user, origin=origin, destination=dest, expires=expires
        )
        RequestTravel.objects.create(user=self.user, origin=origin, destination=dest)

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


class TakeRequestTravelTestCase(TestCase):
    def setUp(self):
        self.user = USER_MODEL.objects.create_user(
            username="XXXXXXXXXXX",
            email="test@gmail.com",
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

    def test_take_request_travel(self):
        origin = Point(0, 0)
        dest = Point(0, 0)

        passager = USER_MODEL.objects.create_user(
            username="XXXXXXXaXXXX",
            email="teaast@gmail.com",
            password="teaastpass12345",
            first_name="test",
            last_name="test",
            is_active=True,
        )

        request_travel = RequestTravel.objects.create(
            user=passager, origin=origin, destination=dest
        )

        travel = take_request_travel(
            request_travel.id, self.user.id, 0, 0, self.vehicle.id
        )

        request_travel = RequestTravel.objects.get(id=request_travel.id)

        self.assertEqual(travel.user, request_travel.user)
        self.assertEqual(travel.driver, self.driver)
        self.assertEqual(Travel.objects.count(), 1)
        self.assertEqual(request_travel.status, RequestTravel.TAKED)
        self.assertNotEqual(travel.user.id, travel.driver.id)

    def test_take_request_travel_self(self):
        origin = Point(0, 0)
        dest = Point(0, 0)

        request_travel = RequestTravel.objects.create(
            user=self.user, origin=origin, destination=dest
        )

        with self.assertRaises(DriverCantTakeRequestTravel):
            take_request_travel(request_travel.id, self.user.id, 0, 0, self.vehicle.id)

    def test_invalid_vehicle(self):
        origin = Point(0, 0)
        dest = Point(0, 0)

        user2 = USER_MODEL.objects.create_user(
            username="XXXXXXXaXXXX",
            email="teaast@gmail.com",
            password="teaastpass12345",
            first_name="test",
            last_name="test",
            is_active=True,
        )
        driver2 = Drivers.objects.create(user=user2, is_active=True)
        vehicle2 = Vehicles.objects.create(
            driver=driver2,
            plate_number="1234",
            model="asas",
            year=1234,
            color="blue",
        )

        request_travel = RequestTravel.objects.create(
            user=self.user, origin=origin, destination=dest
        )

        with self.assertRaises(InvalidVehicleDriver):
            take_request_travel(request_travel.id, self.user.id, 0, 0, vehicle2.id)


class GetTravelByIdTestCase(TestCase):
    def setUp(self) -> None:
        self.user = USER_MODEL.objects.create_user(
            username="XXXXXXXXXXX",
            email="XXXXXXXXXXXXXX",
            password="testpass12345",
            first_name="test",
            last_name="test",
            is_active=True,
        )
        self.driver = Drivers.objects.create(user=self.user, is_active=True)
        self.request_travel = RequestTravel.objects.create(
            user=self.user, origin=Point(0, 0), destination=Point(0, 0)
        )
        self.vehicle = Vehicles.objects.create(
            driver=self.driver,
            plate_number="1234",
            model="asas",
            year=1234,
            color="blue",
        )

    def test_get_travel_by_id(self):
        travel = Travel.objects.create(
            user=self.user,
            driver=self.driver,
            request_travel=self.request_travel,
            origin=self.request_travel.origin,
            destination=self.request_travel.destination,
            vehicle=self.vehicle,
        )

        retrieved_travel = get_travel_by_id(travel.id)

        self.assertEqual(retrieved_travel, travel)
        self.assertEqual(retrieved_travel.user, self.user)
        self.assertEqual(retrieved_travel.driver, self.driver)

    def test_get_travel_by_id_not_found(self):
        with self.assertRaises(TravelDoesNotFound):
            get_travel_by_id(9000)


class CancelTravelTestCase(TestCase):
    def setUp(self) -> None:
        self.user = USER_MODEL.objects.create_user(
            username="XXXXXXXXXXX",
            email="XXXXXXXXXXXXXX",
            password="testpass12345",
            first_name="test",
            last_name="test",
            is_active=True,
        )
        self.user_driver = USER_MODEL.objects.create_user(
            username="XXXXXX1XXXX",
            email="XXXXXXX1XXXXXXX",
            password="testpass12345",
            first_name="test",
            last_name="test",
            is_active=True,
        )
        self.driver = Drivers.objects.create(user=self.user_driver, is_active=True)
        self.request_travel = RequestTravel.objects.create(
            user=self.user, origin=Point(0, 0), destination=Point(0, 0)
        )
        self.vehicle = Vehicles.objects.create(
            driver=self.driver,
            plate_number="1234",
            model="asas",
            year=1234,
            color="blue",
        )

    def test_cancel_travel_user_id(self):
        travel = Travel.objects.create(
            user=self.user,
            driver=self.driver,
            request_travel=self.request_travel,
            origin=self.request_travel.origin,
            destination=self.request_travel.destination,
            vehicle=self.vehicle,
        )

        cancelled_travel = cancel_travel(travel.id, self.user.id)
        travel = Travel.objects.get(id=travel.id)

        self.assertEqual(cancelled_travel.id, travel.id)
        self.assertEqual(travel.status, Travel.CANCELLED)
        self.assertEqual(cancelled_travel.status, Travel.CANCELLED)

    def test_cancel_travel_driver_id(self):
        travel = Travel.objects.create(
            user=self.user,
            driver=self.driver,
            request_travel=self.request_travel,
            origin=self.request_travel.origin,
            destination=self.request_travel.destination,
            vehicle=self.vehicle,
        )

        cancelled_travel = cancel_travel(travel.id, self.driver.user.id)
        travel = Travel.objects.get(id=travel.id)

        self.assertEqual(cancelled_travel.id, travel.id)
        self.assertEqual(travel.status, Travel.CANCELLED)
        self.assertEqual(cancelled_travel.status, Travel.CANCELLED)

    def test_cant_cancel_travel_status(self):
        travel = Travel.objects.create(
            user=self.user,
            driver=self.driver,
            request_travel=self.request_travel,
            origin=self.request_travel.origin,
            destination=self.request_travel.destination,
            status=Travel.DONE,
            vehicle=self.vehicle,
        )

        with self.assertRaises(CannotCancelThisTravel):
            cancel_travel(travel.id, self.user.id)

        self.assertEqual(Travel.objects.get(id=travel.id).status, Travel.DONE)

    def test_cant_cancel_travel_invalid_user(self):
        travel = Travel.objects.create(
            user=self.user,
            driver=self.driver,
            request_travel=self.request_travel,
            origin=self.request_travel.origin,
            destination=self.request_travel.destination,
            vehicle=self.vehicle,
        )

        user2 = USER_MODEL.objects.create_user(
            username="1XXX111XXXXXXXX",
            email="XXXXXXX1X1XXXXXX",
            password="te1stpass12345",
            first_name="test",
            last_name="test",
            is_active=True,
        )

        with self.assertRaises(CannotCancelThisTravel):
            cancel_travel(travel.id, user2.id)

        self.assertEqual(Travel.objects.get(id=travel.id).status, Travel.IN_COURSE)

    def test_cant_cancel_travel_not_found(self):
        with self.assertRaises(TravelDoesNotFound):
            cancel_travel(9000, self.user.id)

    def test_cant_cancel_travel_not_found_user(self):
        travel = Travel.objects.create(
            user=self.user,
            driver=self.driver,
            request_travel=self.request_travel,
            origin=self.request_travel.origin,
            destination=self.request_travel.destination,
            status=Travel.DONE,
            vehicle=self.vehicle,
        )

        with self.assertRaises(UserNotFound):
            cancel_travel(travel.id, uuid4())


class FinishTravelTestCase(TestCase):
    def setUp(self) -> None:
        self.user = USER_MODEL.objects.create_user(
            username="XXXXXXXXXXX",
            email="XXXXXXXXXXXXXX",
            password="testpass12345",
            first_name="test",
            last_name="test",
            is_active=True,
        )
        self.user_driver = USER_MODEL.objects.create_user(
            username="XXXXXX1XXXX",
            email="XXXXXXX1XXXXXXX",
            password="testpass12345",
            first_name="test",
            last_name="test",
            is_active=True,
        )
        self.driver = Drivers.objects.create(user=self.user_driver, is_active=True)

        self.request_travel = RequestTravel.objects.create(
            user=self.user, origin=Point(0, 0), destination=Point(0, 0)
        )
        self.vehicle = Vehicles.objects.create(
            driver=self.driver,
            plate_number="1234",
            model="asas",
            year=1234,
            color="blue",
        )

    def test_finish_travel_user_id(self):
        travel = Travel.objects.create(
            user=self.user,
            driver=self.driver,
            request_travel=self.request_travel,
            origin=self.request_travel.origin,
            destination=self.request_travel.destination,
            vehicle=self.vehicle,
        )
        conf_travel = ConfirmationTravel.objects.create(
            travel=travel,
            user=None,
            driver=self.driver,
        )

        confirmed_travel = finish_travel(travel.id, self.user.id)

        self.assertEqual(confirmed_travel.travel.status, Travel.DONE)
        self.assertEqual(confirmed_travel.user, self.user)
        self.assertEqual(confirmed_travel.travel.id, travel.id)
        self.assertEqual(confirmed_travel.driver, self.driver)
        self.assertEqual(conf_travel.id, confirmed_travel.id)

    def test_finish_travel_driver_id(self):
        travel = Travel.objects.create(
            user=self.user,
            driver=self.driver,
            request_travel=self.request_travel,
            origin=self.request_travel.origin,
            destination=self.request_travel.destination,
            vehicle=self.vehicle,
        )
        conf_travel = ConfirmationTravel.objects.create(
            travel=travel,
            user=self.user,
            driver=None,
        )

        confirmed_travel = finish_travel(travel.id, self.user_driver.id)

        self.assertEqual(confirmed_travel.travel.status, Travel.DONE)
        self.assertEqual(confirmed_travel.user, self.user)
        self.assertEqual(confirmed_travel.travel.id, travel.id)
        self.assertEqual(confirmed_travel.driver, self.driver)
        self.assertEqual(conf_travel.id, confirmed_travel.id)

    def test_finish_travel_first_confirmation_user_id(self):
        travel = Travel.objects.create(
            user=self.user,
            driver=self.driver,
            request_travel=self.request_travel,
            origin=self.request_travel.origin,
            destination=self.request_travel.destination,
            vehicle=self.vehicle,
        )

        confirmed_travel = finish_travel(travel.id, self.user.id)

        self.assertNotEqual(confirmed_travel.travel.status, Travel.DONE)
        self.assertEqual(confirmed_travel.user, self.user)
        self.assertEqual(confirmed_travel.travel.id, travel.id)
        self.assertEqual(confirmed_travel.driver, None)
        self.assertEqual(ConfirmationTravel.objects.count(), 1)

    def test_finish_travel_first_confirmation_driver_id(self):
        travel = Travel.objects.create(
            user=self.user,
            driver=self.driver,
            request_travel=self.request_travel,
            origin=self.request_travel.origin,
            destination=self.request_travel.destination,
            vehicle=self.vehicle,
        )

        confirmed_travel = finish_travel(travel.id, self.user_driver.id)

        self.assertNotEqual(confirmed_travel.travel.status, Travel.DONE)
        self.assertEqual(confirmed_travel.driver, self.driver)
        self.assertEqual(confirmed_travel.travel.id, travel.id)
        self.assertEqual(confirmed_travel.user, None)
        self.assertEqual(ConfirmationTravel.objects.count(), 1)

    def test_cant_finish_travel(self):
        travel = Travel.objects.create(
            user=self.user,
            driver=self.driver,
            request_travel=self.request_travel,
            origin=self.request_travel.origin,
            destination=self.request_travel.destination,
            status=Travel.DONE,
            vehicle=self.vehicle,
        )

        with self.assertRaises(CannotFinishThisTravel):
            finish_travel(travel.id, self.user_driver.id)

        self.assertEqual(ConfirmationTravel.objects.count(), 0)
