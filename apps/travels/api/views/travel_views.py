from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from oauth2_provider.contrib.rest_framework.permissions import TokenHasReadWriteScope

from drf_spectacular.utils import extend_schema

from apps.travels.api.serializers.travel_serializers import (
    TravelSerializer,
    TakeRequestTravelSerializer,
    ConfirmationTravelSerializer,
)
from apps.travels.services import (
    take_request_travel,
    get_travel_by_id,
    cancel_travel,
    finish_travel,
)
from apps.travels.permissions import IsDriverActivePermission
from apps.travels.tasks import send_email_to_users


class TakeRequestTravelApiView(APIView):
    permission_classes = (
        IsAuthenticated,
        TokenHasReadWriteScope,
        IsDriverActivePermission,
    )

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
        vehicle_id = serializer.data.get("vehicle_id", None)

        travel = take_request_travel(
            request_travel_id, request.user.id, long, lat, vehicle_id
        )
        send_email_to_users.delay(
            "Your travel request has been taken!",
            "Your travel request has been taken by {0}, the travel id is {1}".format(
                travel.driver.driver_name, travel.id
            ),
            [travel.user.email],
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


class CancelTravelApiView(APIView):
    permission_classes = (IsAuthenticated, TokenHasReadWriteScope)

    @extend_schema(responses={200: TravelSerializer}, request=None)
    def post(self, request, travel_id: int):
        travel = cancel_travel(travel_id, request.user.id)
        send_email_to_users.delay(
            "Your travel has been cancelled!",
            "Your travel has been cancelled by {0}".format(
                request.user.get_full_name()
            ),
            [travel.user.email, travel.driver.user.email],
        )

        return Response(TravelSerializer(travel).data, status=status.HTTP_200_OK)


class FinishTravelApiView(APIView):
    permission_classes = (IsAuthenticated, TokenHasReadWriteScope)

    @extend_schema(responses={200: ConfirmationTravelSerializer}, request=None)
    def post(self, request, travel_id: int):
        confirmation_travel = finish_travel(travel_id, request.user.id)
        msg = (
            "Your travel has been confirmed by {0}. Travel is done."
            if confirmation_travel.check_driver and confirmation_travel.check_user
            else "Your travel has been confirmed by {0}."
        )

        send_email_to_users.delay(
            "Your travel has been confirmed!",
            msg.format(request.user.get_full_name()),
            [confirmation_travel.user.email, confirmation_travel.driver.user.email],
        )

        return Response(
            ConfirmationTravelSerializer(confirmation_travel).data,
            status=status.HTTP_200_OK,
        )
