from rest_framework.generics import RetrieveUpdateAPIView

from drf_registration.utils.common import import_string, import_string_list
from drf_registration.settings import drfr_settings
from drf_registration.utils.users import get_all_users, get_user_serializer


class ProfileSerializer(get_user_serializer()):

    def __init__(self, *args, **kwargs):
        
        if kwargs.get('context'):
            request = kwargs['context'].get('request', None)

            if request and getattr(request, 'method', None) == 'PUT':
                kwargs['partial'] = True

        super(ProfileSerializer, self).__init__(*args, **kwargs)


class ProfileView(RetrieveUpdateAPIView):

    permission_classes = import_string_list(drfr_settings.PROFILE_PERMISSION_CLASSES)
    serializer_class = import_string(drfr_settings.PROFILE_SERIALIZER)
    queryset = get_all_users()

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):

        for field in drfr_settings.USER_WRITE_ONLY_FIELDS:

            if field in request.data.keys():

                request.data._mutable = True

                request.data.pop(field)

                request.data._mutable = False

        if 'password' in request.data.keys():
            request.data._mutable = True
            self.request.user.set_password(request.data.pop('password')[0])
            self.request.user.save()
            request.data._mutable = False

        return super(ProfileView, self).update(request, *args, **kwargs)