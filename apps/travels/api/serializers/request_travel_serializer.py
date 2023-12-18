from rest_framework.serializers import Serializer, IntegerField, FloatField
from rest_framework_gis.serializers import ModelSerializer

from apps.travels.models import RequestTravel


class RequestTravelSerializer(ModelSerializer):
    class Meta:
        model = RequestTravel
        fields = "__all__"


class RequestTravelQuerySerializer(Serializer):
    radius = IntegerField(max_value=RequestTravel.MAX_RADIUS, min_value=0)
    latitude = FloatField()
    longitude = FloatField()
