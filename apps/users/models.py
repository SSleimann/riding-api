from typing import Any
import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models.fields import EmailField, BooleanField, UUIDField, CharField
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):
    def create_superuser(
        self,
        username: str,
        email: str | None,
        password: str | None,
        **extra_fields: Any,
    ) -> Any:
        user = super().create_superuser(username, email, password, **extra_fields)
        user.is_verified = True
        user.save(update_fields=["is_verified"])

        return user


# Create your models here.
class User(AbstractUser):
    id = UUIDField(_("uuid id"), default=uuid.uuid4, editable=False, primary_key=True)

    email = EmailField(
        _("email address"),
        unique=True,
        help_text=_("Required. Enter a valid email."),
        error_messages={
            "unique": _("A user with that email address  already exists."),
        },
    )

    is_verified = BooleanField(
        _("is verified"),
        default=False,
        help_text=_("Set to true when the user have verified its email address."),
    )

    first_name = CharField(_("first name"), max_length=150)
    last_name = CharField(_("last name"), max_length=150)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = CustomUserManager()

    def get_short_name(self) -> str:
        return self.username

    def set_verified(self) -> None:
        self.is_verified = True
        self.save(update_fields=["is_verified"])

    def __str__(self) -> str:
        return "User: {username}".format(username=self.username)
