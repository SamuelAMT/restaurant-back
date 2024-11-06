from api.custom_auth import auth_router
from restaurant.api import restaurant_router
from restaurant_customer.api import restaurant_customer_router
from reservation.api import reservation_router

__all__ = [
    "auth_router",
    "restaurant_router",
    "restaurant_customer_router",
    "reservation_router",
]
