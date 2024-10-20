from django.urls import path
from ninja import NinjaAPI
from api.custom_auth import auth_router
from restaurant.api import restaurant_router
from restaurant_customer.api import restaurant_customer_router
from reservation.api import reservation_router

app_name = "api-v1"

api = NinjaAPI()


api.add_router("/auth/", auth_router)
api.add_router("/restaurant/", restaurant_router)
api.add_router("/restaurant-customer/", restaurant_customer_router)
api.add_router("/reservations/", reservation_router)

urlpatterns = [
    path("api/v1/", api.urls),
]
