from django.urls import path
from .views import api

# URLConf for restaurant app
urlpatterns = [
    path('api/', api.urls),
]