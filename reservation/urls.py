from django.urls import path
from . import views

app_name = "reservation"

urlpatterns = [
    path("", views.index, name="index"),
    path("restaurant/<uuid:restaurant_id>/reservation/", views.create_reservation, name="create_reservation"),
]
