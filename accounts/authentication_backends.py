from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.core.cache import cache

User = get_user_model()


class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        if not email or not password:
            return

        cache_key = 'login_code_{}'.format(email)
        verify_code = cache.get(cache_key)

        if verify_code != password:
            return

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        return user
