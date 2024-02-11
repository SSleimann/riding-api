from rest_framework.permissions import BasePermission

from apps.drivers.models import Drivers
from apps.drivers.service import set_user_driver_inactive


class IsDriverActivePermission(BasePermission):
    def has_permission(self, request, view):
        try:
            obj = Drivers.objects.values("is_active", "vehicles").get(user=request.user)
        except Drivers.DoesNotExist:
            return False

        if obj.get("is_active", False) and obj.get("vehicles", None) is None:
            set_user_driver_inactive(request.user.id)
            return False

        return bool(request.user and obj.get("is_active", False))


class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and obj.user == request.user)
