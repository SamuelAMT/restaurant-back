from django.urls import path
from custom_auth import views

app_name = 'custom_auth'

urlpatterns = [
    # Restaurant Account URLs (admin by default)
    path('testing/', views.testing_endpoints, name='testing_endpoints'),
    path("account/register/<str:uidb64>/<str:token>/", views.create_account, name="account_register"),
    path('account/register/', views.create_account, name='account_register'),  # Admin account registration
    path('account/setup-password/<str:token>/', views.setup_password, name='account_setup_password'),
    path('account/login/', views.login, name='account_login'),
    path('account/logout/', views.logout, name='account_logout'),
    path('account/password-reset/', views.request_password_reset, name='account_password_reset'),
    path('account/password-reset-confirm/<uidb64>/<token>/', views.reset_password, name='account_password_reset_confirm'),
    path('account/change-password/', views.change_password_view, name='account_change_password'),

    # Custom User URLs (created by admin)
    path('user/register/', views.create_user, name='user_register'),  # Custom user registration
    path('user/setup-password/<str:token>/', views.setup_password, name='user_setup_password'),
    path('user/login/', views.login, name='user_login'),
    path('user/logout/', views.logout, name='user_logout'),
    path('user/password-reset/', views.request_password_reset, name='user_password_reset'),
    path('user/password-reset-confirm/<uidb64>/<token>/', views.reset_password, name='user_password_reset_confirm'),
    path('user/change-password/', views.change_password_view, name='user_change_password'),
]
