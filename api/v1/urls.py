from django.urls import path
from ninja import NinjaAPI
from .restaurant import router as restaurant_router

app_name = 'api_v1'

api = NinjaAPI(title="Restaurant API v1", urls_namespace='restaurant-api')
api.add_router('/restaurant/', restaurant_router)

urlpatterns = [
    path("", api.urls),
    #path("openapi/", api.openapi_url),
    #path("swagger/", api.swagger_ui),
]
