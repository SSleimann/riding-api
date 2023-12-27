from datetime import timedelta

from django.utils.timezone import now

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


class RequestTravelCreationSerializer(ModelSerializer):
    """This class needs to be passed the "context" argument with the user

    Eg: RequestTravelCreationSerializer(..., context={"user": user})
    """

    def create(self, validated_data):
        user = self.context.get("user", None)
        
        request_travel = RequestTravel.objects.create(**validated_data, user=user)

        return request_travel

    class Meta:
        model = RequestTravel
        fields = ("origin", "destination")
