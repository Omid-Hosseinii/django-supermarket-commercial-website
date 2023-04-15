from django.urls import path
from .views import *
#----------------------------------------------------------------------------

app_name='accounts'

urlpatterns = [
    path('register/',RegisterUserView.as_view(),name='user_register'),
    path('verify-register/',VerifyRegisterUserView.as_view(),name='user_veryify_register'),
    path('login/',LoginUserView.as_view(),name='user_login'),
    path('logout-user/',LogoutUserView.as_view(),name='user_logout'),
    path('remmember-password/',RemmeberedPasswordView.as_view(),name='remmember_password'),
    path('change-password/',ChangePasswordView.as_view(),name='change_password'),
    path('user_panel',UserPanelView.as_view(),name='user_panel'),
    path('user_panel_last_order',user_panel_last_order,name='user_panel_last_order'),
    path('user_panel_update',UserPanelUpdateView.as_view(),name='user_panel_update'),
    path('user_panel_payment',peyment_history,name='user_panel_payment'),
    path('change_password_up',ChangePasswordUserPanelView.as_view(),name='change_password_up'),
]
