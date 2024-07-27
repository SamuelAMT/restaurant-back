from django.urls import path
from api.v1.restaurant import router as restaurant_router

urlpatterns = [
    path('', restaurant_router.urls),
]
