from rest_framework_gis.serializers import ModelSerializer

from rest_framework.serializers import Serializer, IntegerField, FloatField

from apps.travels.models import Travel


class TravelSerializer(ModelSerializer):
    class Meta:
        model = Travel
        fields = "__all__"


class TakeRequestTravelSerializer(Serializer):
    longitude = FloatField()
    latitude = FloatField()
