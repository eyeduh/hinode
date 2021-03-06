from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import password_validation
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_registration.settings import drfr_settings
from drf_registration.tokens import activation_token
from drf_registration.utils.common import import_string, import_string_list
from drf_registration.utils.email import send_verify_email, send_email_welcome
from drf_registration.utils.users import (
    get_user_profile_data,
    get_user_serializer,
    has_user_activate_token,
    has_user_verify_code,
    set_user_verified,
    get_user_from_uid,
)
from drf_registration.utils.domain import get_current_domain


class RegisterSerializer(get_user_serializer()):

    def validate_password(self, value):

        password_validation.validate_password(value, self.instance)
        return value

    def create(self, validated_data):

        user = super().create(validated_data)
        user.set_password(validated_data['password'])

        if has_user_activate_token() or has_user_verify_code():
            set_user_verified(user, False)
        else:
            set_user_verified(user, True)
        user.save()
        return user


class RegisterView(CreateAPIView):

    permission_classes = import_string_list(
        drfr_settings.REGISTER_PERMISSION_CLASSES)
    serializer_class = import_string(drfr_settings.REGISTER_SERIALIZER)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        data = get_user_profile_data(user)

        domain = get_current_domain(request)

        if has_user_activate_token() or has_user_verify_code():
            send_verify_email(user, domain)
        else:
            send_email_welcome(user)

        return Response(data, status=status.HTTP_201_CREATED)


class VerifyView(APIView):
    pass

class ActivateView(View):

    def get(self, request, uidb64, token):

        user = get_user_from_uid(uidb64)

        if user and activation_token.check_token(user, token):
            set_user_verified(user)

            send_email_welcome(user)

            if drfr_settings.USER_ACTIVATE_SUCSSESS_TEMPLATE:
                return render(request, drfr_settings.USER_ACTIVATE_SUCSSESS_TEMPLATE) # pragma: no cover
            return HttpResponse(_('Your account has been activate successfully.'))

        if drfr_settings.USER_ACTIVATE_FAILED_TEMPLATE:
            return render(request, drfr_settings.USER_ACTIVATE_FAILED_TEMPLATE) # pragma: no cover
        return HttpResponse(_('Either the provided activation token is '
                              'invalid or this account has already been activated.'))