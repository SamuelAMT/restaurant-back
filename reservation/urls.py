from django.urls import path
from .core import views

app_name = "reservation"

urlpatterns = [
    path("", views.index, name="index"),
]