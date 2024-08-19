from django.urls import path
from . import views

app_name = "restaurant_customer"

urlpatterns = [
    path('', views.customer, name="customer"),
]