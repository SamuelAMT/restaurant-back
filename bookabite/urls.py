from django.contrib import admin
from django.urls import include, path
import debug_toolbar
from ninja import NinjaAPI
from .views import homepage_view, err_404_view
from api.custom_auth import auth_router
from restaurant.api import restaurant_router
from restaurant_customer.api import restaurant_customer_router
from reservation.api import reservation_router
from django.conf.urls import handler404

app_name = "bookabite"

api = NinjaAPI(
    title="BookABite API",
    version="1.0.0",
    description="API for restaurant management and reservations",
    docs_url="/docs/",
)

api.add_router("/auth/", auth_router, tags=["Authentication"])
api.add_router("/restaurant/", restaurant_router, tags=["Restaurant"])
api.add_router("/restaurant-customer/", restaurant_customer_router, tags=["Customer"])
api.add_router("/reservations/", reservation_router, tags=["Reservations"])

urlpatterns = [
    path("", homepage_view, name="homepage"),
    path("admin/", admin.site.urls),
    path("custom_auth/", include("custom_auth.urls", namespace="auth")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api/", api.urls),
]

handler404 = "bookabite.views.err_404_view"
