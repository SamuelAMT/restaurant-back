from django.urls import path
from ninja import NinjaAPI
from .views import register, login_view, logout_view, csrf

api = NinjaAPI(title="Auth API v1", urls_namespace="auth-api")

urlpatterns = [
    path("csrf/", csrf, name="csrf"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("api/", api.urls),
    # path("api/openapi/", api.openapi_url),
    # path("api/swagger/", api.swagger_ui),
]
