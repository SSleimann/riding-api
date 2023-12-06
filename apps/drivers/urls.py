from django.urls import path

from apps.drivers.api.views import (
    ActivateDriverApiView,
    InactiveDriverApiView,
    DriverInfoApiView,
    DriverMeInfoApiView,
    CreateDriverApiView,
)

app_name = "drivers"

urlpatterns = [
    path("create/", CreateDriverApiView.as_view(), name="driver_create"),
    path("driverme/", DriverMeInfoApiView.as_view(), name="driver_me_info"),
    path("activate/", ActivateDriverApiView.as_view(), name="driver_activate"),
    path("inactive/", InactiveDriverApiView.as_view(), name="driver_inactivate"),
    path("driver/<str:username>/", DriverInfoApiView.as_view(), name="driver_info"),
]
