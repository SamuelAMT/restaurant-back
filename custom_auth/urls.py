from django.urls import path
from custom_auth import views

app_name = 'custom_auth'

urlpatterns = [
    path('register/', views.create_user, name='register'),
    path('setup-password/<str:token>/', views.setup_password, name='setup_password'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('password-reset/', views.request_password_reset, name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', views.reset_password, name='password_reset_confirm'),
    path('change-password/', views.change_password, name='change_password'),
]
