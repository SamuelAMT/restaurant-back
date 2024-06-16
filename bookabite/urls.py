from django.urls import path
from . import views

# URLConf for BookABite app
urlpatterns = [
    path('home/', views.index, name="index"),
]