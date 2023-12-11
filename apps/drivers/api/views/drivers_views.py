from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404

from oauth2_provider.contrib.rest_framework.permissions import TokenHasReadWriteScope

from drf_spectacular.utils import extend_schema

from apps.drivers.service import (
    set_user_driver_active,
    set_user_driver_inactive,
    get_driver_by_user_id,
)
from apps.drivers.api.serializers.driver_serializer import (
    DriverSerializer,
    CreateDriverSerializer,
)
from apps.drivers.models import Drivers


class CreateDriverApiView(APIView):
    permission_classes = (IsAuthenticated, TokenHasReadWriteScope)

    @extend_schema(
        request=None, responses={200: DriverSerializer}, description="Create driver"
    )
    def post(self, request):
        data = {"user": request.user.id}
        serializer = CreateDriverSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        driver = serializer.save()

        serialized_data = DriverSerializer(driver).data

        return Response(data=serialized_data, status=status.HTTP_201_CREATED)


class DriverInfoApiView(APIView):
    permission_classes = (IsAuthenticated, TokenHasReadWriteScope)

    @extend_schema(
        responses={200: DriverSerializer},
        description="Get driver info",
    )
    def get(self, request, username):
        driver = get_object_or_404(Drivers, user__username=username)

        serializer = DriverSerializer(driver)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class DriverMeInfoApiView(APIView):
    permission_classes = (IsAuthenticated, TokenHasReadWriteScope)

    @extend_schema(
        responses={200: DriverSerializer},
        description="Get driver me info",
    )
    def get(self, request):
        user_id = request.user.id
        driver = get_driver_by_user_id(user_id)

        serializer = DriverSerializer(driver)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ActivateDriverApiView(APIView):
    permission_classes = (IsAuthenticated, TokenHasReadWriteScope)

    @extend_schema(
        request=None,
        responses={200: DriverSerializer},
        description="Sets the driver to active if has vehicles",
    )
    def put(self, request):
        user_id = request.user.id
        driver = set_user_driver_active(user_id)

        serializer = DriverSerializer(driver)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class InactiveDriverApiView(APIView):
    permission_classes = (IsAuthenticated, TokenHasReadWriteScope)

    @extend_schema(
        request=None,
        responses={200: DriverSerializer},
        description="Set inactive driver",
    )
    def put(self, request):
        user_driver_id = request.user.id
        driver = set_user_driver_inactive(user_driver_id)

        serializer = DriverSerializer(driver)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
