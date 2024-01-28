from datetime import timedelta

from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from apps.drivers.models import Drivers, Vehicles


def request_travel_exp_time():
    return now() + timedelta(minutes=RequestTravel.DELETE_TIME_MIN)


# Create your models here.
class RequestTravel(models.Model):
    DELETE_TIME_MIN = 30
    MAX_RADIUS = 100

    PENDING = "P"
    TAKED = "T"

    CHOICES_STATUS = (
        (PENDING, _("Pending")),
        (TAKED, _("Taked")),
    )

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="req_travels"
    )
    origin = models.PointField(srid=4326, geography=True)
    destination = models.PointField(srid=4326, geography=True)
    created_time = models.DateTimeField(default=now)
    status = models.CharField(
        _("request travel's status"),
        max_length=1,
        choices=CHOICES_STATUS,
        default=PENDING,
    )
    expires = models.DateTimeField(default=request_travel_exp_time)

    @property
    def distance_m(self):
        return self.origin.distance(self.destination) * 1000

    @property
    def is_expired(self):
        return now() >= self.expires

    def __str__(self):
        return "RequestTravel id {0}, origin: {1}".format(self.id, self.origin.coords)


class Travel(models.Model):
    DONE = "D"
    IN_COURSE = "I"
    CANCELLED = "C"

    CHOICES_STATUS = (
        (DONE, _("Done travel")),
        (IN_COURSE, _("Travel in course")),
        (CANCELLED, _("Cancelled travel")),
    )

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name="travels",
        null=True,
        blank=True,
    )
    driver = models.ForeignKey(
        Drivers,
        on_delete=models.SET_NULL,
        related_name="travels",
        null=True,
        blank=True,
    )
    request_travel = models.OneToOneField(
        RequestTravel,
        on_delete=models.SET_NULL,
        related_name="travel",
        null=True,
        blank=True,
    )
    vehicle = models.ForeignKey(
        Vehicles,
        on_delete=models.SET_NULL,
        related_name="travels",
        null=True,
        blank=True,
    )

    origin = models.PointField(srid=4326, geography=True)
    destination = models.PointField(srid=4326, geography=True)
    taked_date = models.DateTimeField(default=now)

    status = models.CharField(
        _("travels status"),
        max_length=1,
        choices=CHOICES_STATUS,
        default=IN_COURSE,
    )

    @property
    def distance_m(self):
        return self.origin.distance(self.destination) * 1000

    def __str__(self):
        return "Travel id {0}, origin: {1}".format(self.id, self.origin.coords)


class ConfirmationTravel(models.Model):
    travel = models.OneToOneField(
        Travel, on_delete=models.CASCADE, related_name="confirmation"
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name="confirmations",
        null=True,
        blank=True,
    )
    driver = models.ForeignKey(
        Drivers,
        on_delete=models.SET_NULL,
        related_name="confirmations",
        null=True,
        blank=True,
    )

    created_time = models.DateTimeField(default=now)

    def __str__(self):
        return "ConfirmationTravel id {0}, travel: {1}".format(self.id, self.travel.id)
