from django.urls import path, include
from .custom_auth import auth_router

app_name = "api"

urlpatterns = [
    path("v1/", include("api.v1.urls", namespace="api-v1")),
    path('auth/', auth_router.urls),
]
