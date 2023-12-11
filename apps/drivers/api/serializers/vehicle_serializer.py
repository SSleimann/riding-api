from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

from apps.drivers.models import Vehicles
from apps.drivers.exceptions import TooManyVehiclesException

class VehiclesSerializer(serializers.ModelSerializer):
    driver = serializers.SerializerMethodField()
    
    class Meta:
        model = Vehicles
        fields = ("id", "driver", "plate_number", "model", "year", "color")
    
    @extend_schema_field(OpenApiTypes.STR)
    def get_driver(self, obj):
        return obj.driver.driver_name


class VehiclesCreationSerializer(serializers.ModelSerializer):
    """ This class needs to be passed the "context" argument with the driver
    
    Eg: VehiclesCreationSerializer(..., context={"driver": driver})
    """
    
    class Meta:
        model = Vehicles
        fields = ("plate_number", "model", "year", "color")
    
    def validate(self, data):
        driver = self.context.get("driver", None)
        
        if driver.vehicles.count() >= 2:
            raise serializers.ValidationError({"vehicles": _("The driver has already 2 vehicles")})
        
        return data
    
    def create(self, validated_data):
        driver = self.context.get("driver", None)
        
        try:
            vehicle = Vehicles.objects.create(**validated_data, driver=driver)
        except TooManyVehiclesException as e: 
            raise serializers.ValidationError({"vehicles": _(e.msg)})
        
        return vehicle