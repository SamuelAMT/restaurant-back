from django.urls import path
from ninja import NinjaAPI
from .restaurant import router as restaurant_router
from .auth import router as auth_router

api = NinjaAPI()
api.add_router('/restaurants/', restaurant_router)
api.add_router('/auth/', auth_router)

urlpatterns = [
    path("", api.urls),
]
