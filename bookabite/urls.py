from django.contrib import admin
from django.urls import include, path
from ninja import NinjaAPI
from .views import homepage_view, err_404_view
from api.auth.admin import admin_auth_router
from api.auth.user import user_auth_router
from address.api import address_router
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

api.add_router("/auth/admin/", admin_auth_router, tags=["Admin Authentication"])
api.add_router("/auth/", user_auth_router, tags=["User Authentication"])
api.add_router("/address/", address_router, tags=["Address"])
api.add_router("/restaurant/", restaurant_router, tags=["Restaurant"])
api.add_router("/restaurant-customer/", restaurant_customer_router, tags=["Customer"])
api.add_router("/reservations/", reservation_router, tags=["Reservations"])

urlpatterns = [
    path("", homepage_view, name="homepage"),
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path("__debug__/", include("debug_toolbar.urls")),
]

handler404 = "bookabite.views.err_404_view"
