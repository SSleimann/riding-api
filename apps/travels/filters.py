from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

from rest_framework.filters import BaseFilterBackend

from django_filters.filterset import FilterSet

from apps.travels.models import RequestTravel
from apps.travels.api.serializers.request_travel_serializer import (
    RequestTravelQuerySerializer,
)


class RequestTravelDistanceToRadiusFilter(BaseFilterBackend):
    latitude_param = "latitude"
    longitude_param = "longitude"
    radius_param = "radius"

    def _get_filter_point(self, serializer_data):
        longitude = serializer_data.get(self.longitude_param)
        latitude = serializer_data.get(self.latitude_param)

        point = Point(longitude, latitude)

        return point

    def filter_queryset(self, request, queryset, view):
        query_strings = {
            "latitude": request.query_params.get(self.latitude_param, None),
            "longitude": request.query_params.get(self.longitude_param, None),
            "radius": request.query_params.get(
                self.radius_param, RequestTravel.MAX_RADIUS
            ),
        }

        serializer = RequestTravelQuerySerializer(data=query_strings)
        serializer.is_valid(raise_exception=True)

        point = self._get_filter_point(serializer.data)
        radius = serializer.data.get(self.radius_param)

        queryset = queryset.filter(origin__distance_lte=(point, D(km=radius)))

        return queryset

    def get_schema_operation_parameters(self, view):
        return [
            {
                "name": self.latitude_param,
                "required": True,
                "in": "query",
                "schema": {"type": "number", "format": "float"},
                "description": f"Represents latitude point.",
            },
            {
                "name": self.longitude_param,
                "required": True,
                "in": "query",
                "schema": {"type": "number", "format": "float"},
                "description": f"Represents longitude point.",
            },
            {
                "name": self.radius_param,
                "required": False,
                "in": "query",
                "schema": {
                    "type": "integer",
                    "maximum": RequestTravel.MAX_RADIUS,
                    "minimum": 0,
                    "example": 50,
                },
                "description": f"Represents radius in kilometers.",
            },
        ]

class RequestTravelFilter(FilterSet):
    
    class Meta:
        model = RequestTravel
        fields = ("status", )