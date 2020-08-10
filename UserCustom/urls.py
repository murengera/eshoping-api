from django.urls import path
from UserCustom import views


urlpatterns = [

    path("login/", views.login, name="auth_token_login"),

    path("buyer_register/", views.buyer_register, name="user_register"),

    path('manager-register', views.manager_register, name='register_manager'),
    path('forget-password', views.forgot_password),
    path('update-groups/', views.update_groups),
    path('verify-user', views.verify, name='verify_account'),
    path('resend-verification-code', views.resend_verification, name='resend_verification'),
    path('send-reset-code', views.send_reset_code, name='send-reset-code'),
    path('reset-password', views.reset_password, name='reset-password'),
    path('update-profile', views.update_profile, name='update_profile'),
    path('activate_account',views.activate_account),
    path('users/', views.UserList.as_view(), name='users_list'),
    path('users/<slug:pk>', views.UserDetail.as_view(), name='users_detail')



]
