from django.urls import path, include
from .api import restaurant_router
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet

app_name = "restaurant"

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)

urlpatterns = [
    path("api/", restaurant_router.urls),
    path('', include(router.urls)),
]
