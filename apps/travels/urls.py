from django.urls import path

from apps.travels.api.views.request_travel_views import (
    ListRequestTravelApiView,
    ListRequestTravelUserApiView,
    CreateRequestTravelApiView,
    RequestTravelApiView
)

from apps.travels.api.views.travel_views import (
    TakeRequestTravelApiView
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
    path("rt/<int:id>/", RequestTravelApiView.as_view(), name="request_travel_get_delete"),
    
    path("travel/take/<int:request_travel_id>/", TakeRequestTravelApiView.as_view(), name="travel_take_request_travel")
]
