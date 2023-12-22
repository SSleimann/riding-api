from django.urls import path

from apps.travels.api.views.request_travel_views import (
    ListRequestTravelApiView,
    ListRequestTravelUserApiView,
    CreateRequestTravelApiView,
    RequestTravelApiView
)

app_name = "travels"

urlpatterns = [
    path("rt/", ListRequestTravelApiView.as_view(), name="request_travel_list"),
    path(
        "rt/user/",
        ListRequestTravelUserApiView.as_view(),
        name="request_travel_user_list",
    ),
    path(
        "rt/create/", CreateRequestTravelApiView.as_view(), name="request_travel_create"
    ),
    path("rt/<int:id>/", RequestTravelApiView.as_view(), name="request_travel_get_delete")
]
