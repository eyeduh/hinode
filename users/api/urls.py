from django.urls import path
from .views import (
    profile_detail_api_view,
    # user_login_view,
    # user_register_view,
    # obtain_token_view,
)


urlpatterns = [
    path('<str:username>/', profile_detail_api_view),
    path('<str:username>/follow', profile_detail_api_view),
 ]
