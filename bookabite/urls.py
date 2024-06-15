from django.urls import path
from . import views

# URL Configuration for BookABite app
urlpatterns = [
    path("home/", views.index, name="index"),
]