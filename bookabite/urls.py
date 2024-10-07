from django.contrib import admin
from django.urls import include, path
import debug_toolbar
from ninja import NinjaAPI
from .views import router as restaurant_router

api = NinjaAPI()
api.add_router("/myapp/", restaurant_router)
app_name = "bookabite"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.v1.urls", namespace="api")),
    path("auth/", include("custom_auth.urls")),
    path("accounts/", include("allauth.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api/openapi/", api.openapi_url),
    path("api/swagger/", api.swagger_ui),
]
