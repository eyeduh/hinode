from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model as django_get_user_model

from rest_framework.authtoken.models import Token

from drf_registration.settings import drfr_settings
from drf_registration.utils.common import import_string


def get_user_model():

    return django_get_user_model()


def get_all_users():

    return get_user_model().objects.all()


def get_user_serializer():

    return import_string(drfr_settings.USER_SERIALIZER)


def get_user_token(user):

    token, created = Token.objects.get_or_create(user=user)

    return token


def remove_user_token(user):

    Token.objects.filter(user=user).delete()


def get_user_profile_data(user):

    serializer = import_string(drfr_settings.USER_SERIALIZER)
    data = serializer(user).data

    if has_user_verified(user):
        data['token'] = get_user_token(user).key

    return data


def has_user_activate_token():

    return drfr_settings.USER_ACTIVATE_TOKEN_ENABLED


def has_user_verify_code():

    return drfr_settings.USER_VERIFY_CODE_ENABLED


def has_user_verified(user):

    return get_user_verified(user)


def get_user_verified(user):

    return getattr(user, drfr_settings.USER_VERIFY_FIELD)


def set_user_verified(user, verified=True):

    setattr(user, drfr_settings.USER_VERIFY_FIELD, verified)
    user.save()


def generate_user_uid(user):

    return urlsafe_base64_encode(force_bytes(user.pk))


def generate_uid_and_token(user, token_generator=None):

    token_generator = token_generator or default_token_generator

    return {
        'uidb64': generate_user_uid(user),
        'token': token_generator.make_token(user)
    }


def get_user_from_uid(uidb64):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
        return user
    except:
        return None