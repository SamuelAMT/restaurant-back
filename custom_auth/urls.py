from django.urls import path
from custom_auth import views

app_name = 'custom_auth'

urlpatterns = [
    # Account URLs
    path('account/register/', views.create_account, name='account_register'),
    path('account/setup-password/<str:token>/', views.setup_account_password, name='account_setup_password'),
    path('account/login/', views.account_login, name='account_login'),
    path('account/logout/', views.account_logout, name='account_logout'),
    path('account/password-reset/', views.account_request_password_reset, name='account_password_reset'),
    path('account/password-reset-confirm/<uidb64>/<token>/', views.account_reset_password, name='account_password_reset_confirm'),
    path('account/change-password/', views.account_change_password, name='account_change_password'),

    # CustomUser URLs
    path('user/register/', views.create_user, name='user_register'),
    path('user/setup-password/<str:token>/', views.setup_user_password, name='user_setup_password'),
    path('user/login/', views.user_login, name='user_login'),
    path('user/logout/', views.user_logout, name='user_logout'),
    path('user/password-reset/', views.user_request_password_reset, name='user_password_reset'),
    path('user/password-reset-confirm/<uidb64>/<token>/', views.user_reset_password, name='user_password_reset_confirm'),
    path('user/change-password/', views.user_change_password, name='user_change_password'),
]