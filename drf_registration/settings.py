from django.test.signals import setting_changed
from drf_registration.utils.common import generate_settings, get_django_settings

PACKAGE_NAME = 'drf_registration'
PACKAGE_OBJECT_NAME = 'DRF_REGISTRATION'

DEFAULT_SETTINGS = {

    'PROJECT_NAME': 'DRF Registration',
    'PROJECT_BASE_URL': 'drf_registration/api',

    'USER_FIELDS': (
        'id',
        'username',
        'email',
        'password',
        'first_name',
        'last_name',
        'is_active',
    ),
    'USER_READ_ONLY_FIELDS': (
        'is_superuser',
        'is_staff',
        'is_active',
    ),
    'USER_WRITE_ONLY_FIELDS': (
        'password',
    ),

    'USER_SERIALIZER': 'drf_registration.api.views.user.UserSerializer',

    'USER_VERIFY_CODE_ENABLED': False,
    'USER_VERIFY_FIELD': 'is_active',

    'USER_ACTIVATE_TOKEN_ENABLED': False,
    'USER_ACTIVATE_SUCSSESS_TEMPLATE': '',
    'USER_ACTIVATE_FAILED_TEMPLATE': '',
    'USER_ACTIVATE_EMAIL_SUBJECT': 'Activate your account',
    'USER_ACTIVATE_EMAIL_TEMPLATE': '',

    'PROFILE_SERIALIZER': 'users.serializers.PublicUserProfileSerializer',
    'PROFILE_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'REGISTER_SERIALIZER': 'users.serializers.PublicUserProfileSerializer',
    'REGISTER_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'REGISTER_SEND_WELCOME_EMAIL_ENABLED': False,
    'REGISTER_SEND_WELCOME_EMAIL_SUBJECT': 'Welcome to the system',
    'REGISTER_SEND_WELCOME_EMAIL_TEMPLATE': '',

    'LOGIN_SERIALIZER': 'drf_registration.api.views.login.LoginSerializer',
    'LOGIN_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],

    'LOGIN_USERNAME_FIELDS': ['username', 'email',],

    'LOGOUT_REMOVE_TOKEN': False,

    'CHANGE_PASSWORD_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'CHANGE_PASSWORD_SERIALIZER': 'drf_registration.api.views.change_password.ChangePasswordSerializer',

    'RESET_PASSWORD_ENABLED': True,
    'RESET_PASSWORD_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'RESET_PASSWORD_SERIALIZER': 'drf_registration.api.views.reset_password.ResetPasswordSerializer',
    'RESET_PASSWORD_EMAIL_SUBJECT': 'Reset Password',
    'RESET_PASSWORD_EMAIL_TEMPLATE': '',
    'RESET_PASSWORD_CONFIRM_TEMPLATE': '',
    'RESET_PASSWORD_SUCCESS_TEMPLATE': '',

    'FACEBOOK_LOGIN_ENABLED': False,
    'GOOGLE_LOGIN_ENABLED': False,

    'SET_PASSWORD_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'SET_PASSWORD_SERIALIZER': 'drf_registration.api.views.set_password.SetPasswordSerializer',
}

drfr_settings = generate_settings(get_django_settings(), DEFAULT_SETTINGS)


def settings_changed_handler(*args, **kwargs):

    setting_values = kwargs['value']
    setting_key = kwargs['setting']

    if setting_values and setting_key == PACKAGE_OBJECT_NAME:
        for prop in setting_values:
            drfr_settings[prop] = setting_values[prop]


setting_changed.connect(settings_changed_handler)
