from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from oauth2_provider.contrib.rest_framework.permissions import TokenHasReadWriteScope

from drf_spectacular.utils import extend_schema

from apps.drivers.service import (
    delete_vehicle_by_id_and_driver_id,
    get_driver_by_user_id
)
from apps.drivers.api.serializers.vehicle_serializer import (
    VehiclesSerializer,
    VehiclesCreationSerializer,
)
from apps.drivers.exceptions import VehicleDoesNotExistsException

from apps.drivers.models import Vehicles

class VehiclesCreationApiView(APIView):
    permission_classes = (IsAuthenticated, TokenHasReadWriteScope)
    
    @extend_schema(
        request=VehiclesCreationSerializer,
        responses={201: VehiclesSerializer},
        description="Create a vehicle"
    )
    def post(self, request):
        driver = get_driver_by_user_id(request.user.id)
        
        serializer = VehiclesCreationSerializer(data=request.data, context={"driver": driver})
        serializer.is_valid(raise_exception=True)
        
        vehicle = serializer.save()
        
        return Response(data=VehiclesSerializer(vehicle).data, status=status.HTTP_201_CREATED)

class VehiclesListApiView(APIView):
    permission_classes = (IsAuthenticated, TokenHasReadWriteScope)
    
    @extend_schema(
        responses={200: VehiclesSerializer},
        description="Get vehicles info"
    )
    def get(self, request):
        driver = get_driver_by_user_id(request.user.id)
        vehicles_serializer = VehiclesSerializer(driver.vehicles.all(), many=True)
        
        return Response(data=vehicles_serializer.data, status=status.HTTP_200_OK)
    
class VehiclesDeleteApiView(APIView):
    permission_classes = (IsAuthenticated, TokenHasReadWriteScope)
    
    @extend_schema(
        responses={204: None},
        description="Delete vehicle by id"
    )
    def delete(self, request, uuid):
        driver = get_driver_by_user_id(request.user.id)
        
        delete_vehicle_by_id_and_driver_id(vehicle_id=uuid, driver_id=driver.id)
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class VehiclesDetailApiView(APIView):
    permission_classes = (IsAuthenticated, TokenHasReadWriteScope)
    
    @extend_schema(
        responses={200: VehiclesSerializer},
        description="Get vehicle by id"
    )
    def get(self, request, uuid):
        try:
            vehicle = Vehicles.objects.get(id=uuid)
        except Vehicles.DoesNotExist:
            raise VehicleDoesNotExistsException
            
        vehicle_serializer = VehiclesSerializer(vehicle)
        
        return Response(data=vehicle_serializer.data, status=status.HTTP_200_OK)