from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('reservations/', views.reservations_view, name='reservations'),
    path('customers/', views.customers_view, name='customers'),
    path('settings/', views.settings_view, name='settings'),
    #path('profile/', views.profile_view, name='profile'),
]
