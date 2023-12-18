from django.urls import path

from apps.travels.api.views.request_travel_views import ListRequestTravelApiView, ListRequestTravelUserApiView

app_name = "travels"

urlpatterns = [
    path("rt/", ListRequestTravelApiView.as_view(), name="request_travel_list"),
    path("rt/user/", ListRequestTravelUserApiView.as_view(), name="request_travel_user_list"),
]
