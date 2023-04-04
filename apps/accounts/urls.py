from django.urls import path
from .views import *
#----------------------------------------------------------------------------

app_name='accounts'

urlpatterns = [
    path('register/',RegisterUserView.as_view(),name='user_register'),
    path('verify-register/',VerifyRegisterUserView.as_view(),name='user_veryify_register'),
    path('login-user/',LoginUserView.as_view(),name='user_login'),
    path('logout-user/',LogoutUserView.as_view(),name='user_logout'),
    path('remmember-password/',RemmeberedPasswordView.as_view(),name='remmember_password'),
    path('change-password/',ChangePasswordView.as_view(),name='change_password'),
]
