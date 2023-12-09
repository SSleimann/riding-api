
import uuid

from typing import Any

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings

from apps.drivers.exceptions import TooManyVehiclesException

# Create your models here.
class VehicleManager(models.Manager):
    
    def create(self, **kwargs: Any) -> Any:
        if self._get_driver_vehicles_count(kwargs.get("driver")) >= Drivers.MAX_VEHICLES:
            raise TooManyVehiclesException
        
        return super().create(**kwargs)
    
    def _get_driver_vehicles_count(self, driver) -> int:
        driver_vehicles = self.get_queryset().filter(driver=driver)
        
        return driver_vehicles.count()

class Drivers(models.Model):
    ACTIVE = "A"
    BUSY = "B"
    MAX_VEHICLES = 2

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

class Vehicles(models.Model):
    id = models.UUIDField(_("id"), primary_key=True, default=uuid.uuid4, editable=False)
    driver = models.ForeignKey(Drivers, on_delete=models.CASCADE, related_name="vehicles")
    plate_number = models.CharField(_("plate number"), max_length=10)
    model = models.CharField(_("model"), max_length=100)
    year = models.IntegerField(_("year"))
    color = models.CharField(_("color"), max_length=100)

    objects = VehicleManager()
    
    def __str__(self) -> str:
        return f"{self.model} {self.year} {self.color}"
    

# class Rating(models.Model):
#     driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
#     from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     value = models.FloatField(_("rating"), validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

#     class Meta:
#         constraints = [
#             CheckConstraint(check=~Q(from_user=F("driver")), name="prevent self rating"),
#             UniqueConstraint(fields=["driver", "from_user"], name="unique rating")
#         ]
