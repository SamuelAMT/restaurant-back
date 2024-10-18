from django.urls import path
from .api import restaurant_customer_router

app_name = "restaurant_customer"

urlpatterns = [
    path("api/", restaurant_customer_router.urls),
]
