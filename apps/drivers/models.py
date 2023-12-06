import uuid

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import CheckConstraint, Q, F, UniqueConstraint, Avg

# Create your models here.


class Drivers(models.Model):
    ACTIVE = "A"
    BUSY = "B"

    status_choices = [
        (ACTIVE, _("Active")),
        (BUSY, _("Busy")),
    ]

    id = models.UUIDField(_("id"), primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(_("is active"), default=False)
    status = models.CharField(
        _("driver status"), max_length=1, choices=status_choices, default=ACTIVE
    )

    @property
    def driver_name(self) -> str:
        return self.user.get_full_name()

    def has_vehicles(self) -> bool:
        return self.vehicles.exists()

    def set_active(self) -> None:
        self.is_active = True
        self.save()

    def set_inactive(self) -> None:
        self.is_active = False
        self.save()


# class Rating(models.Model):
#     driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
#     from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     value = models.FloatField(_("rating"), validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

#     class Meta:
#         constraints = [
#             CheckConstraint(check=~Q(from_user=F("driver")), name="prevent self rating"),
#             UniqueConstraint(fields=["driver", "from_user"], name="unique rating")
#         ]
