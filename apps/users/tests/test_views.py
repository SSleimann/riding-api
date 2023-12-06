from datetime import timedelta

from django.test import TestCase
from django.core import mail
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.conf import settings

from rest_framework.test import APIClient

from apps.users.security import create_jwt_token

from riding.celery import app


class TestUserRegisterView(TestCase):
    def setUp(
        self,
    ) -> None:
        self.factory = APIClient()
        app.conf.update(CELERY_ALWAYS_EAGER=True)

    def test_user_creation(self):
        payload = {
            "username": "test1",
            "password": "passwordSecure",
            "confirm_password": "passwordSecure",
            "email": "testemai1l@gmail.com",
            "first_name": "pablo",
            "last_name": "pedro",
        }

        res = self.factory.post(
            reverse_lazy("users:user_register"), data=payload, format="json"
        )
        u = get_user_model().objects.get(email=payload["email"])

        self.assertEqual(res.status_code, 201)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIsNotNone(res.data.get("username"))
        self.assertEqual(u.username, payload["username"])
        self.assertFalse(u.is_verified)


class TestUserVerifyView(TestCase):
    def setUp(self):
        self.factory = APIClient()
        self.user = get_user_model().objects.create_user(
            username="test3",
            password="passwdo",
            email="testemail3@gmail.com",
            first_name="pablo",
            last_name="pedro",
        )

    def test_verify_user(self):
        token = create_jwt_token(
            {"type": "_email_confirmation", "user_username": self.user.username},
            settings.JWT_SECRET_KEY,
            timedelta(minutes=1),
        )
        payload = {"token": token}

        res = self.factory.post(
            reverse_lazy("users:user_verify"), data=payload, format="json"
        )
        res_data = res.data
        u = get_user_model().objects.get(email=res_data["email"])

        self.assertTrue(u.is_verified)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["username"], u.username)
        self.assertEqual(res_data["email"], u.email)
        self.assertEqual(res_data["is_verified"], u.is_verified)
