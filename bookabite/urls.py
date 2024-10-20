from django.contrib import admin
from django.urls import include, path
import debug_toolbar
from ninja import NinjaAPI
from api.custom_auth import auth_router

app_name = "bookabite"

api = NinjaAPI()

api.add_router("/auth/", auth_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.v1.urls", namespace="api-v1")),  # API Versioning
    path("__debug__/", include("debug_toolbar.urls")),
    path("api/openapi/", api.openapi),
    path("api/swagger/", api.swagger_ui),
]