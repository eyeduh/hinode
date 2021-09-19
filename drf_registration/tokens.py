from django.contrib.auth.tokens import PasswordResetTokenGenerator
try:
    from django.utils import six
except:
    import six

from drf_registration.utils.users import get_user_verified


class CustomAccountActivationTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(get_user_verified(user))
        )


class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):

    pass


activation_token = CustomAccountActivationTokenGenerator()
reset_password_token = CustomPasswordResetTokenGenerator()