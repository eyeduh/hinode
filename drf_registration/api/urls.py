from django.urls import path

from .views import (
    login, 
    logout, 
    profile, 
    register, 
    reset_password, 
    change_password, 
    set_password
)

urlpatterns = [
    path('login/', login.LoginView.as_view(), name='login'),
    path('login/social/', login.SocialLoginView.as_view(), name='login_social'),
    path('logout/', logout.LogoutView.as_view(), name='logout'),
    path('register/', register.RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', register.ActivateView.as_view(), name='activate'),
    path('verify/', register.VerifyView.as_view(), name='verify'),
    path('profile/', profile.ProfileView.as_view(), name='profile'),
    path('change-password/', change_password.ChangePasswordView.as_view(), name='change_password'),
    path('reset-password/', reset_password.ResetPasswordView.as_view(), name='reset_password'),
    path('reset-password/<uidb64>/<token>/', reset_password.ResetPasswordConfirmView.as_view(), name='reset_password_confirm'),
    path('reset-password/complete/', reset_password.ResetPasswordCompleteView.as_view(), name='reset_password_complete'),
    path('set-password/', set_password.SetPasswordView.as_view(), name='set_password'),
]
