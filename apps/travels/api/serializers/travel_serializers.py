from rest_framework_gis.serializers import ModelSerializer

from rest_framework.serializers import (
    Serializer,
    UUIDField,
    FloatField,
)

from apps.travels.models import Travel
from apps.drivers.models import Vehicles


class TravelSerializer(ModelSerializer):
    class Meta:
        model = Travel
        fields = "__all__"


class TakeRequestTravelSerializer(Serializer):
    longitude = FloatField()
    latitude = FloatField()
    vehicle_id = UUIDField()
