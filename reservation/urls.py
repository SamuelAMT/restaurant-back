from django.urls import path
from . import views

# URLConf for reservation app
urlpatterns = [
    path('', views.index, name="index"),
]