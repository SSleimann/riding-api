from jose import jwt

from django.test import TestCase
from django.core import mail
from django.contrib.auth import get_user_model
from django.conf import settings

from riding.celery import app

from apps.users.api.serializers.user_serializer import UserRegisterSerializer
from apps.users.api.serializers.token_serializer import TokenVerificationSerializer


class UserRegisterSerializerTestCase(TestCase):
    def setUp(self) -> None:
        app.conf.update(CELERY_TASK_ALWAYS_EAGER=True)

    def test_serializer_create(self):
        payload = {
            "username": "testpepe",
            "email": "trest@gmail.com",
            "password": "testpass12345",
            "confirm_password": "testpass12345",
            "first_name": "test",
            "last_name": "test",
        }

        serializer = UserRegisterSerializer(data=payload)
        serializer.is_valid()
        u = serializer.save()

        self.assertTrue(u)
        q = get_user_model().objects.get(username=payload["username"])

        self.assertEqual(q.username, u.username)
        self.assertEqual(len(mail.outbox), 1)

    def test_invalid_password_match(self):
        payload = {
            "username": "testpepe",
            "email": "trest@gmail.com",
            "password": "testpass12345",
            "confirm_password": "testpass123451",
            "first_name": "test",
            "last_name": "test",
        }
        serializer = UserRegisterSerializer(data=payload)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors.keys(), set(["password", "confirm_password"])
        )


class TokenVerificationSerializerTestCase(TestCase):
    def setUp(self) -> None:
        payload = {
            "username": "te1stpepe",
            "email": "trest1@gmail.com",
            "password": "testpass12345",
            "first_name": "test",
            "last_name": "test",
            "is_active": False,
        }
        self.user = get_user_model().objects.create_user(**payload)

    def test_verification(self):
        payload = {
            "token": jwt.encode(
                {"user_username": self.user.username, "type": "_email_confirmation"},
                settings.JWT_SECRET_KEY,
            )
        }

        serializer = TokenVerificationSerializer(data=payload)
        serializer.is_valid()
        u = serializer.save()

        self.assertEqual(u.username, self.user.username)
        self.assertTrue(u.is_verified)

    def test_invalid_token_type(self):
        payload = {"token": jwt.encode({"type": "1"}, settings.JWT_SECRET_KEY)}

        serializer = TokenVerificationSerializer(data=payload)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors.keys(), {"token"})

    def test_invalid_token_decoding(self):
        payload = {"token": jwt.encode({"type": "_email_confirmation"}, "1")}

        serializer = TokenVerificationSerializer(data=payload)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors.keys(), {"token"})
