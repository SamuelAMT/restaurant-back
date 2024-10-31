from django.contrib import admin
from django.urls import include, path
import debug_toolbar
from ninja import NinjaAPI
from ninja.openapi.urls import get_openapi_urls

app_name = "bookabite"

api = NinjaAPI()

openapi_urls = get_openapi_urls(api)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.v1.urls", namespace="api-v1")), # API Versioning
    path('custom_auth/', include('custom_auth.urls', namespace='auth')),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api/openapi/", include(openapi_urls)),
]
