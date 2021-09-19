from django.conf import settings
from django.utils.module_loading import import_string as django_import_string


class AttributeDict(dict):

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def get_django_settings(settings_name='DRF_REGISTRATION'):

    return getattr(settings, settings_name, {})


def generate_settings(user_settings, default_settings):

    result = {}

    for prop in default_settings:
        result[prop] = user_settings.get(prop, default_settings[prop])

    return AttributeDict(result)


def import_string(dotted_path):

    return django_import_string(dotted_path)


def import_string_list(dotted_paths):

    return [import_string(dotted_path) for dotted_path in dotted_paths]