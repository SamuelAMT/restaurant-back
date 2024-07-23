from ninja import NinjaAPI

api = NinjaAPI()

# Import routers to register them
from .restaurant import router as restaurant_router

# Add routers to the API
api.add_router("/restaurant/", restaurant_router)
