from django.urls import path
from . import views

# URLConf for restaurant app
urlpatterns = [
    path('home/', views.index, name="index"),
]