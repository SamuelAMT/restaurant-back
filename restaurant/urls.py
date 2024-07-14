from django.urls import path
from . import views

# URLConf for restaurant app
urlpatterns = [
    path('home/', views.index, name="index"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('calendar/', views.calendar, name="calendar"),
    path('customer-list/', views.customer_list, name="customer_list"),
    path('settings/', views.settings, name="settings"),
]