from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _


class MessagesDrfConfig(BaseAppConfig):
    name = "django_messages_drf"
    label = "django_messages_drf"
    verbose_name = _("Django Messages DRF")