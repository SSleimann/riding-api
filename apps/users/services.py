from uuid import UUID

from django.contrib.auth import get_user_model

from apps.users.models import User
from apps.users.exceptions import UserNotFound


def get_user_by_id(user_id: UUID) -> User:
    model = get_user_model()

    try:
        user = model.objects.get(id=user_id)
    except model.DoesNotExist:
        raise UserNotFound

    return user
