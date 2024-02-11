from datetime import timedelta

from django.db.models import Q
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from oauth2_provider.contrib.rest_framework.permissions import TokenHasReadWriteScope

from drf_spectacular.openapi import OpenApiParameter, OpenApiTypes
from drf_spectacular.utils import extend_schema

from django_filters.utils import translate_validation

from apps.travels.permissions import IsDriverActivePermission, IsOwnerPermission
from apps.travels.models import RequestTravel
from apps.travels.api.serializers.request_travel_serializer import (
    RequestTravelSerializer,
    RequestTravelCreationSerializer,
)
from apps.travels.filters import (
    RequestTravelDistanceToRadiusFilter,
    RequestTravelFilter,
)
from apps.travels.services import (
    get_request_travel_by_id,
    delete_request_travel_by_id_and_user_id,
)


class ListRequestTravelApiView(GenericAPIView):
    permission_classes = (
        IsAuthenticated,
        TokenHasReadWriteScope,
        IsDriverActivePermission,
    )
    filter_backends = (RequestTravelDistanceToRadiusFilter,)

    @extend_schema(
        responses={200: RequestTravelSerializer},
        parameters=[
            OpenApiParameter(
                name="radius",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                default=RequestTravel.MAX_RADIUS,
                description="Radius for find request travels",
            ),
            OpenApiParameter(
                name="latitude",
                type=OpenApiTypes.FLOAT,
                location=OpenApiParameter.QUERY,
                required=True,
            ),
            OpenApiParameter(
                name="longitude",
                type=OpenApiTypes.FLOAT,
                location=OpenApiParameter.QUERY,
                required=True,
            ),
        ],
        description="Retrieves all request travels near a point with a radius",
    )
    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = RequestTravelSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = RequestTravel.objects.filter(
            Q(status=RequestTravel.PENDING) and Q(expires__gte=timezone.now())
        )

        return queryset


class ListRequestTravelUserApiView(APIView):
    permission_classes = (IsAuthenticated, TokenHasReadWriteScope)

    @extend_schema(
        responses={200: RequestTravelSerializer},
        parameters=[
            OpenApiParameter(
                name="status",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Status of the request travel. P (Pending), T (Taked)",
            )
        ],
        description="Retrieves all request travels of the user",
    )
    def get(self, request):
        user = request.user

        filter = RequestTravelFilter(request.GET, queryset=user.req_travels.all())

        if not filter.is_valid():
            raise translate_validation(filter.errors)

        request_travels = filter.qs

        serializer = RequestTravelSerializer(request_travels, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateRequestTravelApiView(APIView):
    permission_classes = (IsAuthenticated, TokenHasReadWriteScope)

    @extend_schema(
        request=RequestTravelCreationSerializer,
        responses={201: RequestTravelSerializer},
        description="Create a request travel",
    )
    def post(self, request):
        user = self.request.user

        serializer = RequestTravelCreationSerializer(
            data=request.data, context={"user": user}
        )
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()

        data = RequestTravelSerializer(obj).data

        return Response(data, status=status.HTTP_201_CREATED)


class RequestTravelApiView(APIView):
    permission_classes = (IsAuthenticated, TokenHasReadWriteScope)

    @extend_schema(
        responses={200: RequestTravelSerializer},
        description="Retrieve a request travel",
    )
    def get(self, request, id):
        request_travel = get_request_travel_by_id(id)

        serializer = RequestTravelSerializer(request_travel)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses={204: None}, description="Delete a request travel")
    def delete(self, request, id):
        request_travel = get_request_travel_by_id(id)
        self.check_object_permissions(request, request_travel)

        delete_request_travel_by_id_and_user_id(request_travel.id, request.user.id)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        permission_classes = self.permission_classes

        if self.request.method == "DELETE":
            permission_classes = (IsOwnerPermission,) + permission_classes

        return [permission() for permission in permission_classes]
