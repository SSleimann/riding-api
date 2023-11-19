from rest_framework.serializers import ModelSerializer, CharField

from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core import exceptions

from apps.users.models import User
from apps.users.tasks import send_verification_email

from rest_framework import serializers


class UserModelReadSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_verified",
        )
        read_only_fields = ("is_active", "is_verified", "email")


class UserRegisterSerializer(ModelSerializer):
    password = CharField(
        min_length=1, max_length=64, trim_whitespace=False, write_only=True
    )

    confirm_password = CharField(
        min_length=1, max_length=64, trim_whitespace=False, write_only=True
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "confirm_password",
            "is_active",
            "is_verified",
        )
        read_only_fields = ["is_active", "is_verified"]

    def validate(self, attrs):
        password = attrs.get("password")
        password_conf = attrs.get("confirm_password")

        if password and password_conf and password != password_conf:
            msg = _("Passwords do not match.")
            raise serializers.ValidationError(
                {"password": msg, "confirm_password": msg}
            )

        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})

        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = get_user_model().objects.create_user(**validated_data)

        send_verification_email.delay(user.id)

        return user
