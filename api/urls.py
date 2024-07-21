from django.urls import path
from ninja import NinjaAPI
from .restaurant import router as restaurant_router
from .reservation import router as reservation_router
#from .restaurant_customer import router as restaurant_customer_router

api = NinjaAPI()

@api.get("/hello")
def hello(request):
    return {"message": "Hello world"}

api.add_router('/restaurant/', restaurant_router)
api.add_router('/reservation/', reservation_router)
#api.add_router('/restaurant_customer/', restaurant_customer_router)

urlpatterns = [
    path("api/", api.urls),
]
