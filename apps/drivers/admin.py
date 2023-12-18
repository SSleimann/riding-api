from django.contrib import admin

from apps.drivers.models import Vehicles, Drivers


class DriversAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "is_active", "status")
    list_filter = ("user", "is_active")


class VehiclesAdmin(admin.ModelAdmin):
    list_display = ("id", "driver", "plate_number", "model", "year", "color")
    list_filter = ("driver",)


# Register your models here.
admin.site.register(Vehicles, VehiclesAdmin)
admin.site.register(Drivers, DriversAdmin)
