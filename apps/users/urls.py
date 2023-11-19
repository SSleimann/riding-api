from django.urls import path

from apps.users.api.views import UserRegisterView, UserVerifiyView

app_name = "users"

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user_register"),
    path("verify/", UserVerifiyView.as_view(), name="user_verify"),
]
