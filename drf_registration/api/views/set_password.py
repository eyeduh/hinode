from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import password_validation

from rest_framework import status
from rest_framework import serializers
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response


from drf_registration.settings import drfr_settings
from drf_registration.utils.users import get_user_profile_data
from drf_registration.utils.common import import_string, import_string_list


class SetPasswordSerializer(serializers.Serializer):

    password = serializers.CharField()

    def validate_password(self, password):

        user = self.context['request'].user
        if user.password:
            raise serializers.ValidationError(_('Your password is already existed.'))
        password_validation.validate_password(password, user)
        return password

    def save(self, **kwargs):
        password = self.validated_data['password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


class SetPasswordView(UpdateAPIView):

    permission_classes = import_string_list(drfr_settings.SET_PASSWORD_PERMISSION_CLASSES)
    serializer_class = import_string(drfr_settings.SET_PASSWORD_SERIALIZER)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        data = get_user_profile_data(user)

        return Response(data, status=status.HTTP_200_OK)
        