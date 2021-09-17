from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView

from users.serializers import PublicUserProfileSerializer

from accounts.serializers import RegisterSerializer, ObtainTokenSerializer

User = get_user_model()


class UserLoginAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = PublicUserProfileSerializer


class UserRegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UserObtainTokenAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ObtainTokenSerializer


user_login_view = UserLoginAPIView.as_view()
user_register_view = UserRegisterAPIView.as_view()
obtain_token_view = UserObtainTokenAPIView.as_view()
