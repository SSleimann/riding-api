from django.contrib.gis import admin

from apps.travels.models import RequestTravel


class RequestTravelAdmin(admin.GISModelAdmin):
    list_display = (
        "id",
        "user",
        "origin",
        "destination",
        "created_time",
    )
    list_filter = ("user", "created_time")


# Register your models here.
admin.site.register(RequestTravel, RequestTravelAdmin)
