from django.urls import path

from apps.travels.api.views.request_travel_views import ListRequestTravelApiView

app_name = "travels"

urlpatterns = [
    path("rt/", ListRequestTravelApiView.as_view(), name="request_travel_list"),
]
