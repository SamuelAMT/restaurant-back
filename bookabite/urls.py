from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from ninja import NinjaAPI
from bookabite.core.views import homepage_view, err_404_view
from bookabite.templates.core.views import debug_templates
from api.auth.routers import admin_auth_router, user_auth_router
from address.api import address_router
from restaurant.api import restaurant_router
from restaurant.api.routes.customer import customer_router
from restaurant.api.routes.dashboard import dashboard_router
from restaurant.api.routes.profile import profile_router
from restaurant.api.routes.settings import settings_router
from restaurant_customer.api import restaurant_customer_router
from reservation.api import reservation_router
from restaurant.api.routes.unit import unit_router

api = NinjaAPI(
    title="BookABite API",
    version="1.0.0",
    description="API for restaurant management and reservations",
    docs_url="/docs/",
)

# API Routes
api.add_router("/auth/admin/", admin_auth_router, tags=["Admin Authentication"])
api.add_router("/auth/", user_auth_router, tags=["User Authentication"])
api.add_router("/address/", address_router, tags=["Address"])
api.add_router("/restaurant/", restaurant_router, tags=["Restaurant"])
api.add_router("/restaurant/customer/", customer_router, tags=["Restaurant"])
api.add_router("/restaurant/settings/", settings_router, tags=["Restaurant"])
api.add_router("/restaurant/dashboard/", dashboard_router, tags=["Restaurant"])
api.add_router("/restaurant/profile/", profile_router, tags=["Restaurant"])
api.add_router("/restaurant-customer/", restaurant_customer_router, tags=["Customer"])
api.add_router("/reservations/", reservation_router, tags=["Reservations"])
api.add_router("/restaurant/", unit_router, tags=["Unit"])

urlpatterns = [
    path("", homepage_view, name="homepage"),
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path("debug-templates/", debug_templates, name="debug-templates"),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

handler404 = "bookabite.core.views.err_404_view"