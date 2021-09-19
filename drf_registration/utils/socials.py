import requests
from rest_framework.utils import json

from drf_registration.settings import drfr_settings
from drf_registration.constants import (
    FACEBOOK_PROVIDER,
    FACEBOOK_AUTH_URL,
    FACEBOOK_FIELDS,
    GOOGLE_AUTH_URL,
    GOOGLE_PROVIDER,
)


def is_valid_provider(provider):

    if is_facebook_provider(provider) and drfr_settings.FACEBOOK_LOGIN_ENABLED:
        return True

    if is_google_provider(provider) and drfr_settings.GOOGLE_LOGIN_ENABLED:
        return True

    return False


def is_facebook_provider(provider):

    return provider == FACEBOOK_PROVIDER


def is_google_provider(provider):

    return provider == GOOGLE_PROVIDER


def get_user_info(provider, access_token):

    if is_facebook_provider(provider):
        request_api = FACEBOOK_AUTH_URL
        params = {
            'access_token': access_token,
            'fields': FACEBOOK_FIELDS
        }

    if is_google_provider(provider):
        request_api = GOOGLE_AUTH_URL
        params = {
            'id_token': access_token
        }

    req = requests.get(request_api, params=params)
    data = json.loads(req.text)

    return None if 'error' in data else data


def enable_has_password():

    return drfr_settings.FACEBOOK_LOGIN_ENABLED or drfr_settings.GOOGLE_LOGIN_ENABLED