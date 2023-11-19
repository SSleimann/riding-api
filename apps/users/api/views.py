import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST

from rest_framework.request import Request

from oauth2_provider.views.mixins import OAuthLibMixin
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.models import get_access_token_model

from drf_yasg.utils import swagger_auto_schema

from apps.users.api.serializers.user_serializer import (
    UserRegisterSerializer,
    UserModelReadSerializer,
)
from apps.users.api.serializers.token_serializer import TokenVerificationSerializer

class UserRegisterView(APIView):
    @swagger_auto_schema(
        request_body=UserRegisterSerializer,
        responses={"201": UserRegisterSerializer, "400": "Bad Request"},
        operation_description="Creates a new user",
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=HTTP_201_CREATED)


class UserVerifiyView(APIView):
    @swagger_auto_schema(
        request_body=TokenVerificationSerializer,
        responses={"200": UserModelReadSerializer, "400": "Bad Request"},
        operation_description="Verifies a user",
    )
    def post(self, request):
        token_serializer = TokenVerificationSerializer(data=request.data)
        token_serializer.is_valid(raise_exception=True)
        user = token_serializer.save()

        return Response(UserModelReadSerializer(user).data, status=HTTP_200_OK)


class TokenApiView(OAuthLibMixin, APIView):
    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS
    
    def post(self, request: Request, *args, **kwargs):
        mutable_data = request.data.copy()
        
        #make request._request mutable
        request._request.POST = request._request.POST.copy()
        
        for key, value in mutable_data.items():
            request._request.POST[key] = value
        
        url, headers, body, status = self.create_token_response(request._request)
        content = json.loads(body)
        
            
        return Response(data=content, status=status)
    