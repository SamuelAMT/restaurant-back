from django.contrib import admin
from django.urls import include, path
import debug_toolbar
from ninja import NinjaAPI
from api.custom_auth import auth_router
from restaurant.api import restaurant_router
from restaurant_customer.api import restaurant_customer_router
from reservation.api import reservation_router

app_name = "bookabite"

api = NinjaAPI(
    title="BookABite API",
    version="1.0.0",
    description="API for restaurant management and reservations",
    docs_url="/docs/",
)

api.add_router("/auth/", auth_router)
api.add_router("/restaurant/", restaurant_router)
api.add_router("/restaurant-customer/", restaurant_customer_router)
api.add_router("/reservations/", reservation_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("custom_auth/", include("custom_auth.urls", namespace="auth")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api/", api.urls),
]
