from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView

from drf_registration.utils.users import remove_user_token
from drf_registration.settings import drfr_settings


class LogoutView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):

        if drfr_settings.LOGOUT_REMOVE_TOKEN:
            remove_user_token(self.request.user)

        return Response(status=status.HTTP_204_NO_CONTENT)