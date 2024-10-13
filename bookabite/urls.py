from django.contrib import admin
from django.urls import include, path
import debug_toolbar
from ninja import NinjaAPI
from custom_auth.api import auth_router
# TODO: Veriy if I'm gonna stick with the api app approach or use  an api.py for each app
# TODO: Also, decide if I'm let the router below within move it to api app
from .views import router as restaurant_router

app_name = "bookabite"

api = NinjaAPI()

api.add_router("/auth/", auth_router)
api.add_router("/myapp/", restaurant_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.v1.urls", namespace="api-v1")),
    #path("auth/", include("custom_auth.urls")),
    #path("accounts/", include("allauth.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api/openapi/", api.openapi_url),
    path("api/swagger/", api.swagger_ui),
]
