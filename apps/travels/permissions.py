from rest_framework.permissions import BasePermission

from apps.drivers.models import Drivers


class IsDriverPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            obj = Drivers.objects.values("is_active").get(user=request.user)
        except Drivers.DoesNotExist:
            return False

        return bool(request.user and obj.get("is_active", False))


class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and obj.user == request.user)
