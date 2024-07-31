from django.urls import path
from ninja import NinjaAPI
from .restaurant import router as restaurant_router

api = NinjaAPI(title="Restaurant API v1", urls_namespace='restaurant-api')
api.add_router('/restaurant/', restaurant_router)

urlpatterns = [
    path("", api.urls),
]
