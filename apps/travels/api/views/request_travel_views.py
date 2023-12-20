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

from apps.travels.permissions import IsDriverPermission
from apps.travels.models import RequestTravel
from apps.travels.api.serializers.request_travel_serializer import (
    RequestTravelSerializer,
    RequestTravelCreationSerializer,
)
from apps.travels.filters import (
    RequestTravelDistanceToRadiusFilter,
    RequestTravelFilter,
)


class ListRequestTravelApiView(GenericAPIView):
    permission_classes = (IsAuthenticated, TokenHasReadWriteScope, IsDriverPermission)
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
    )
    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = RequestTravelSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        expired_at = timezone.now() - timedelta(minutes=RequestTravel.DELETE_TIME_MIN)

        queryset = RequestTravel.objects.filter(
            Q(status=RequestTravel.PENDING) and Q(created_time__gte=expired_at)
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
