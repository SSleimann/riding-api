from django.test import TestCase

from apps.users.security import create_jwt_token, decode_jwt_token

from datetime import timedelta

from jose import jwt


class CreateJWTTokenTestCase(TestCase):
    def test_create_jwt_token(self):
        JWT_KEY = "1234"
        to_encode = {"test": 1}
        expire = timedelta(minutes=1)

        token = create_jwt_token(to_encode, JWT_KEY, expire)
        decoded_token = jwt.decode(token, JWT_KEY, algorithms=["HS256"])

        self.assertIsInstance(token, str)
        self.assertEqual(to_encode["test"], decoded_token["test"])


class DecodeJWTTokenTestCAse(TestCase):
    def test_decode_jwt_token(self):
        JWT_KEY = "1234"
        to_encode = {"test": 1}

        token = jwt.encode(to_encode, JWT_KEY, algorithm="HS256")
        decoded_token = decode_jwt_token(token, JWT_KEY)

        self.assertIsInstance(decoded_token, dict)
        self.assertEqual(to_encode["test"], decoded_token["test"])

    def test_error_decode_jwt_token(self):
        JWT_KEY = "1234"
        to_encode = {"test": 1}
        token = jwt.encode(to_encode, JWT_KEY, algorithm="HS256")

        decoded_token = decode_jwt_token(token, "1")

        self.assertIsNone(decoded_token)
