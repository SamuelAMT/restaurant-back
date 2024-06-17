from django.urls import path
from . import views

# URLConf for address app
urlpatterns = [
    path('home/', views.index, name="index"),
]