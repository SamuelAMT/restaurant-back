from django.urls import path
from .api import restaurant_router

app_name = "restaurant"

urlpatterns = [
    path("api/", restaurant_router.urls),
]
