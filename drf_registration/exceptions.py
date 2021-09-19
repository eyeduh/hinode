from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework import status


class NotActivated(APIException):

    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Account is not activated.')
    default_code = 'not-activated'


class LoginFailed(APIException):

    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Login failed wrong user credentials.')
    default_code = 'login-failed'


class UserNotFound(APIException):

    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('User not found.')
    default_code = 'user-not-found'


class InvalidProvider(APIException):

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Provider is invalid or you forgot enable social login.')
    default_code = 'invalid-provider'


class InvalidAccessToken(APIException):

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('This access token is invalid or is already expired.')
    default_code = 'invalid-access-token'


class MissingEmail(APIException):

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Missing email address.')
    default_code = 'missing-email'
    