from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from drf_spectacular.utils import extend_schema

from apps.users.api.serializers.user_serializer import (
    UserRegisterSerializer,
    UserModelReadSerializer,
)
from apps.users.api.serializers.token_serializer import TokenVerificationSerializer


class UserRegisterView(APIView):
    @extend_schema(
        request=UserRegisterSerializer,
        responses={201: UserRegisterSerializer},
        description="Creates a new user",
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=HTTP_201_CREATED)


class UserVerifiyView(APIView):
    @extend_schema(
        request=TokenVerificationSerializer,
        responses={200: UserModelReadSerializer},
        description="Verifies a user",
    )
    def post(self, request):
        token_serializer = TokenVerificationSerializer(data=request.data)
        token_serializer.is_valid(raise_exception=True)
        user = token_serializer.save()

        return Response(UserModelReadSerializer(user).data, status=HTTP_200_OK)
