from django.urls import path

from accounts.api.views import user_login_view, user_register_view, obtain_token_view

urlpatterns = [
    path('login/', user_login_view, name='user_login'),
    path('login/step-1/', user_register_view, name='user_login_step_1'),
    path('login/step-2/', obtain_token_view, name='user_login_step_2'),
]
