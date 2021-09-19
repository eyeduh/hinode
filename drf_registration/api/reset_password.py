
from django.http import Http404
from django.utils.translation import gettext as _
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy

from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from drf_registration.exceptions import UserNotFound
from drf_registration.settings import drfr_settings
from drf_registration.utils.common import import_string, import_string_list
from drf_registration.utils.domain import get_current_domain
from drf_registration.utils.users import get_user_model
from drf_registration.utils.email import send_reset_password_token_email


class ResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate(self, data):

        try:
            user = get_user_model().objects.get(email=data['email'])
        except get_user_model().DoesNotExist:
            raise UserNotFound()
            
        data['user'] = user

        return data


class ResetPasswordView(APIView):

    permission_classes = import_string_list(drfr_settings.RESET_PASSWORD_PERMISSION_CLASSES)
    serializer_class = import_string(drfr_settings.RESET_PASSWORD_SERIALIZER)

    def post(self, request, *args, **kwargs):

        if not drfr_settings.RESET_PASSWORD_ENABLED:
            raise Http404()

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        domain = get_current_domain(request)
        send_reset_password_token_email(user, domain)

        return Response(
            {'detail': _('Password reset e-mail has been sent.')},
            status=status.HTTP_200_OK)


class ResetPasswordConfirmView(PasswordResetConfirmView):

    success_url = reverse_lazy('reset_password_complete')

    if drfr_settings.RESET_PASSWORD_CONFIRM_TEMPLATE:
        template_name = drfr_settings.RESET_PASSWORD_CONFIRM_TEMPLATE


class ResetPasswordCompleteView(PasswordResetCompleteView):

    if drfr_settings.RESET_PASSWORD_SUCCESS_TEMPLATE:
        template_name = drfr_settings.RESET_PASSWORD_SUCCESS_TEMPLATE