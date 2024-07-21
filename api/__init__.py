from ninja import NinjaAPI

api = NinjaAPI()

# Import routers to register them
from .restaurant import router as restaurant_router
from .reservation import router as reservation_router

# Add routers to the API
api.add_router("/restaurants/", restaurant_router)
api.add_router("/reservations/", reservation_router)
