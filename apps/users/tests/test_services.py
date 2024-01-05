from django.test import TestCase

from django.contrib.auth import get_user_model

from apps.users.services import get_user_by_id
from apps.users.exceptions import UserNotFound


class GetUserByIdTestCase(TestCase):
    def test_get_user_by_id(self):
        user = get_user_model().objects.create_user(
            username="te122stpepe",
            email="trest21@gmail.com",
            password="testpass12345",
            first_name="test",
            last_name="test",
            is_active=True,
        )

        retrieved_user = get_user_by_id(user.id)

        self.assertEqual(retrieved_user.id, user.id)
        self.assertEqual(retrieved_user.username, user.username)
        self.assertEqual(retrieved_user.email, user.email)
        self.assertEqual(retrieved_user.first_name, user.first_name)
        self.assertEqual(retrieved_user.last_name, user.last_name)
        self.assertEqual(retrieved_user.is_active, user.is_active)

    def test_get_user_by_id_with_invalid_id(self):
        with self.assertRaises(UserNotFound):
            get_user_by_id(999)
