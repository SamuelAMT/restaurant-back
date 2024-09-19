from django.urls import path
from api.v1.restaurant import router as restaurant_router

app_name = "restaurant"

urlpatterns = [
    path("", restaurant_router.urls),
]
