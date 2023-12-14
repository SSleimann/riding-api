from datetime import timedelta

from django.db.models import Q
from django.utils import timezone

from rest_framework.generics import GenericAPIView 
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from oauth2_provider.contrib.rest_framework.permissions import TokenHasReadWriteScope

from drf_spectacular.utils import extend_schema

from apps.travels.models import RequestTravel
from apps.travels.utils import get_ip_from_request
from apps.travels.api.serializers.request_travel_serializer import RequestTravelSerializer
from apps.travels.filters import RequestTravelDistanceToRadiusFilter


class ListRequestTravelApiView(GenericAPIView):
    #permission_classes = (IsAuthenticated, TokenHasReadWriteScope)
    filter_backends = (RequestTravelDistanceToRadiusFilter, )
    
    @extend_schema(responses={200: RequestTravel})
    def get(self, request):
        
        queryset = self.filter_queryset(self.get_queryset())
        serializer = RequestTravelSerializer(queryset, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_queryset(self):
        expired_at = timezone.now() - timedelta(minutes=RequestTravel.DELETE_TIME_MIN)
        
        queryset = RequestTravel.objects.filter(
            Q(status=RequestTravel.PENDING) and Q(created_time__gte=expired_at)
        ).all()
        
        return queryset