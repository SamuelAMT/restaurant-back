from django.urls import path
from ninja import NinjaAPI
from .restaurant import router as restaurant_router
from api.v1.auth import router as auth_router

app_name = 'api_v1'

api = NinjaAPI(title="Restaurant API v1")
api.add_router('/restaurant/', restaurant_router)
api.add_router('/auth/', auth_router)

urlpatterns = [
    path("", api.urls),
]
