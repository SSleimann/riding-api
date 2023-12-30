from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from oauth2_provider.contrib.rest_framework.permissions import TokenHasReadWriteScope

from drf_spectacular.utils import extend_schema

from apps.travels.api.serializers.travel_serializers import (
    TravelSerializer,
    TakeRequestTravelSerializer,
)
from apps.travels.services import take_request_travel, get_travel_by_id
from apps.travels.tasks import send_email_to_user_by_travel


class TakeRequestTravelApiView(APIView):
    permission_classes = (IsAuthenticated, TokenHasReadWriteScope)

    @extend_schema(
        request=TakeRequestTravelSerializer,
        responses={200: TravelSerializer},
    )
    def post(self, request, request_travel_id: int):
        serializer = TakeRequestTravelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        long, lat = serializer.data.get("longitude", None), serializer.data.get(
            "latitude", None
        )

        travel = take_request_travel(request_travel_id, request.user.id, long, lat)
        send_email_to_user_by_travel.delay(
            travel.id,
            "Your travel request has been taken!",
            "Your travel request has been taken by {0}, the travel id is {1}".format(
                travel.driver.driver_name, travel.id
            ),
        )

        return Response(TravelSerializer(travel).data, status=status.HTTP_200_OK)


class TravelApiView(APIView):
    permission_classes = (IsAuthenticated, TokenHasReadWriteScope)

    @extend_schema(
        responses={200: TravelSerializer},
    )
    def get(self, request, travel_id: int):
        travel = get_travel_by_id(travel_id)

        return Response(TravelSerializer(travel).data, status=status.HTTP_200_OK)
