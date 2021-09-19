from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

from drf_registration.settings import drfr_settings
from drf_registration.utils.common import import_string, import_string_list
from drf_registration.utils.users import (
    get_user_model,
    get_user_profile_data,
    has_user_verified,
    set_user_verified,
)
from drf_registration.utils import socials
from drf_registration.exceptions import (
    NotActivated,
    LoginFailed,
    InvalidProvider,
    MissingEmail,
    InvalidAccessToken,
)


class LoginSerializer(serializers.ModelSerializer):

    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')

    def validate(self, data):
        user = authenticate(**data)
        if user:

            if has_user_verified(user):

                data['user'] = user

                return data
            raise NotActivated()
        raise LoginFailed()


class LoginView(CreateAPIView):

    permission_classes = import_string_list(
        drfr_settings.LOGIN_PERMISSION_CLASSES)
    serializer_class = import_string(drfr_settings.LOGIN_SERIALIZER)

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        update_last_login(None, user)
        data = get_user_profile_data(user)

        return Response(data, status=status.HTTP_200_OK)


class SocialLoginSerializer(serializers.Serializer):

    provider = serializers.CharField()
    access_token = serializers.CharField()

    class Meta:
        fields = ('provider', 'access_token',)


class SocialLoginView(CreateAPIView):

    permission_classes = import_string_list(
        drfr_settings.LOGIN_PERMISSION_CLASSES)
    serializer_class = SocialLoginSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        provider = serializer.data.get('provider', None)

        if not socials.is_valid_provider(provider):
            raise InvalidProvider()

        access_token = serializer.data.get('access_token', None)

        user_data = socials.get_user_info(provider, access_token)

        if not user_data:
            raise InvalidAccessToken()

        if not user_data.get('email'):
            raise MissingEmail()

        User = get_user_model()
        try:
            user = User.objects.get(email=user_data['email'])
        except User.DoesNotExist:
            user = User.objects.create(
                username=user_data['email'],
                email=user_data['email'],
                first_name=user_data.get('first_name'),
                last_name=user_data.get('last_name'),
            )

            set_user_verified(user)

        update_last_login(None, user)
        data = get_user_profile_data(user)

        return Response(data, status=status.HTTP_200_OK)