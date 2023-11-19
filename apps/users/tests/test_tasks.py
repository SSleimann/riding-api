from django.test import TestCase
from django.core import mail
from django.contrib.auth import get_user_model

from apps.users.tasks import send_verification_email
from riding.celery import app


class SendVerificationEmailTestCase(TestCase):
    def setUp(self) -> None:
        app.conf.update(CELERY_TASK_ALWAYS_EAGER=True)
        get_user_model().objects.create_user(
            username="test",
            password="passwdo",
            email="testemail@gmail.com",
            first_name="pablo",
            last_name="pedro",
        )

    def test_send_verification_email(self):
        user = get_user_model().objects.get(email="testemail@gmail.com")

        send_verification_email.delay(user.pk)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Email Verification!")
        self.assertIn(user.username, mail.outbox[0].body)
