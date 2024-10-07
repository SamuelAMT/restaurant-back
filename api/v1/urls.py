from django.urls import path
from ninja import NinjaAPI
from .reservation import reservation_router
from .restaurant import router as restaurant_router

api = NinjaAPI(title="Restaurant API v1:1.0.0")

api = NinjaAPI(title="Restaurant API v1", urls_namespace="restaurant-api")
api.add_router("/reservation/", reservation_router)
api.add_router("/restaurant/", restaurant_router)

urlpatterns = [
    path("", api.urls),
    # path("openapi/", api.openapi_url),
    # path("swagger/", api.swagger_ui),
]
