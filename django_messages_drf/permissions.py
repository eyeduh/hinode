from django.conf import settings

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class DjangoMessageDRFAuthMeta(type):

    def __new__(cls, name, bases, attrs):
        permissions = []
        for base in bases:
            if hasattr(base, 'permissions'):
                permissions.extend(base.permissions)
        attrs['permissions'] = permissions + attrs.get('permissions', [])
        return type.__new__(cls, name, bases, attrs)


class AccessMixin(metaclass=DjangoMessageDRFAuthMeta):

    pass


class DjangoMessageDRFAuthMixin(AccessMixin, APIView): 

    permissions = [IsAuthenticated]
    pagination_class = None

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)
        self.permission_classes = self.permissions
        if self.pagination_class:
            try:
                rest_settings = settings.REST_FRAMEWORK
            except AttributeError:
                rest_settings = {}
            page_size = rest_settings.get('PAGE_SIZE', 50)
            self.pagination_class.page_size = page_size