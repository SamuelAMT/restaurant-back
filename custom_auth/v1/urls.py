from django.urls import path
from custom_auth import views

app_name = 'custom_auth'

urlpatterns = [
    path('register/', views.create_user, name='register'),
    path('setup-password/<str:token>/', views.setup_password, name='setup_password'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('change-password/', views.change_password_view, name='change_password'),
]
