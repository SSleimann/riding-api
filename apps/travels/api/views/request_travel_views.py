from datetime import timedelta

from django.db.models import Q
from django.utils import timezone

from rest_framework.generics import GenericAPIView 
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from oauth2_provider.contrib.rest_framework.permissions import TokenHasReadWriteScope

from drf_spectacular.openapi import OpenApiParameter, OpenApiTypes
from drf_spectacular.utils import extend_schema

from apps.travels.permissions import IsDriverPermission
from apps.travels.models import RequestTravel
from apps.travels.api.serializers.request_travel_serializer import RequestTravelSerializer
from apps.travels.filters import RequestTravelDistanceToRadiusFilter


class ListRequestTravelApiView(GenericAPIView):
    permission_classes = (IsAuthenticated, TokenHasReadWriteScope, IsDriverPermission)
    filter_backends = (RequestTravelDistanceToRadiusFilter, )
    
    @extend_schema(
        responses={200: RequestTravelSerializer},
        parameters=[
            OpenApiParameter(name="radius", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY, required=False, default=RequestTravel.MAX_RADIUS, description="Radius for find request travels"),
            OpenApiParameter(name="latitude", type=OpenApiTypes.FLOAT, location=OpenApiParameter.QUERY, required=True),
            OpenApiParameter(name="longitude", type=OpenApiTypes.FLOAT, location=OpenApiParameter.QUERY, required=True)
        ]
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