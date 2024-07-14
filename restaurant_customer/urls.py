from django.urls import path
from . import views

# URLConf for restaurant app
urlpatterns = [
    path('', views.customer, name="customer"),
]