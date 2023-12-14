from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from apps.drivers.models import Drivers

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
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    origin = models.PointField(srid=4326, geography=True)
    destination = models.PointField(srid=4326, geography=True)
    created_time = models.DateTimeField(default=now)
    status = models.CharField(_("request travel's status"), max_length=1, choices=CHOICES_STATUS, default=PENDING)
    
    @property
    def distance_m(self):
        return self.origin.distance(self.destination) * 1000
    
    def __str__(self):
        return "RequestTravel id {0}, origin: {1}".format(self.id, self.origin.coords)