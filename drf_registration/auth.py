from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from drf_registration.settings import drfr_settings


class MultiFieldsModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:

            assert drfr_settings.LOGIN_USERNAME_FIELDS

            filters = Q()

            for login_field in drfr_settings.LOGIN_USERNAME_FIELDS:
                filters |= Q(**{login_field:username})

            user = get_user_model().objects.get(filters)

        except (get_user_model().DoesNotExist, get_user_model().MultipleObjectsReturned):
            return None
        else:
            if user.check_password(password):
                return user