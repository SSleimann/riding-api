from datetime import timedelta

from django.test import TestCase
from django.contrib.gis.geos import Point
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.test import APIRequestFactory

from apps.travels.models import RequestTravel
from apps.travels.filters import RequestTravelDistanceToRadiusFilter
from apps.travels.api.serializers.request_travel_serializer import (
    RequestTravelQuerySerializer,
)

USER_MODEL = get_user_model()


class TestView(GenericAPIView):
    filter_backends = (RequestTravelDistanceToRadiusFilter,)

    def get_queryset(self):
        expired_at = timezone.now() - timedelta(minutes=RequestTravel.DELETE_TIME_MIN)

        queryset = RequestTravel.objects.filter(
            Q(status=RequestTravel.PENDING) and Q(created_time__gte=expired_at)
        )

        return queryset


class RequestTravelDistanceToRadiusFilterTestCase(TestCase):
    def setUp(self):
        self.user = USER_MODEL.objects.create_user(
            username="te122stpepe",
            email="trest21@gmail.com",
            password="testpass12345",
            first_name="test",
            last_name="test",
            is_active=True,
        )
        self.factory = APIRequestFactory()

    def test_get_filter_point(self):
        filter = RequestTravelDistanceToRadiusFilter()
        serializer = RequestTravelQuerySerializer(
            data=dict(radius=10, latitude=0, longitude=0)
        )
        serializer.is_valid()

        point = filter._get_filter_point(serializer.data)

        self.assertEqual(point.coords, (0, 0))
        self.assertIsInstance(point, Point)

    def test_filter_queryset(self):
        view = TestView()
        view.request = view.initialize_request(
            self.factory.get("/", {"longitude": 0, "latitude": 0, "radius": 100})
        )
        queryset = view.get_queryset()

        obj = RequestTravel.objects.create(
            user=self.user, origin=Point(0, 0), destination=Point(0, 0)
        )

        filter_queryset = view.filter_queryset(queryset)

        self.assertEqual(len(filter_queryset), 1)
        self.assertEqual(filter_queryset[0].id, obj.id)

    def test_filter_queryset_no_long_lat(self):
        view = TestView()
        view.request = view.initialize_request(self.factory.get("/", {"radius": 100}))
        queryset = view.get_queryset()

        with self.assertRaises(ValidationError) as e:
            view.filter_queryset(queryset)

        self.assertEqual(e.exception.detail.keys(), {"latitude", "longitude"})
