from rest_framework.serializers import ModelSerializer, CharField, Serializer

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.conf import settings

from apps.users.security import decode_jwt_token

from rest_framework import serializers


class TokenVerificationSerializer(Serializer):
    token = CharField(
        write_only=True, help_text="Token for verificate account", required=True
    )

    def validate_token(self, value):
        payload = decode_jwt_token(value, settings.JWT_SECRET_KEY)

        if payload is None:
            raise serializers.ValidationError({"token": _("The token is invalid.")})
        
        if payload.get("type", None) != "_email_confirmation":
            raise serializers.ValidationError({"token": _("The token is invalid.")})
        
        if payload.get("user_username", None) is None:
            raise serializers.ValidationError({"token": _("The token is invalid.")})

        self.context["payload"] = payload

        return value

    def save(self, **kwargs):
        payload = self.context["payload"]
        user = get_user_model().objects.get(username=payload.get("user_username", None))

        user.is_verified = True

        user.save()

        return user
