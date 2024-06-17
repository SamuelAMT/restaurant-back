from django.urls import path
from . import views

# URLConf for reservation app
urlpatterns = [
    path('home/', views.index, name="index"),
]