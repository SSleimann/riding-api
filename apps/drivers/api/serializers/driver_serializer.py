from rest_framework import serializers

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

from apps.drivers.models import Drivers


class DriverSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Drivers
        fields = ("user", "is_active", "status")

    @extend_schema_field(OpenApiTypes.STR)
    def get_user(self, obj):
        return obj.user.username


class CreateDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drivers
        fields = ("user",)
