from django.urls import path

from apps.drivers.api.views.drivers_views import (
    ActivateDriverApiView,
    InactiveDriverApiView,
    DriverInfoApiView,
    DriverMeInfoApiView,
    CreateDriverApiView,
)
from apps.drivers.api.views.vehicles_views import (
    VehiclesCreationApiView,
    VehiclesListApiView,
    VehiclesDeleteApiView,
    VehiclesDetailApiView,
)

app_name = "drivers"

driver_urlpatterns = [
    path("create/", CreateDriverApiView.as_view(), name="driver_create"),
    path("driverme/", DriverMeInfoApiView.as_view(), name="driver_me_info"),
    path("activate/", ActivateDriverApiView.as_view(), name="driver_activate"),
    path("inactive/", InactiveDriverApiView.as_view(), name="driver_inactivate"),
    path("driver/<str:username>/", DriverInfoApiView.as_view(), name="driver_info"),
]

vehicles_urlpatterns = [
    path("vehicles/create/", VehiclesCreationApiView.as_view(), name="vehicles_create"),
    path("vehicles/", VehiclesListApiView.as_view(), name="vehicles_list"),
    path(
        "vehicles/delete/<uuid:uuid>/",
        VehiclesDeleteApiView.as_view(),
        name="vehicles_delete",
    ),
    path(
        "vehicles/info/<uuid:uuid>",
        VehiclesDetailApiView.as_view(),
        name="vehicles_detail",
    ),
]

urlpatterns = driver_urlpatterns + vehicles_urlpatterns
