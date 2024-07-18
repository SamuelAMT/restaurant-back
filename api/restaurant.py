from ninja import Router
from pydantic import BaseModel

router = Router()

class RestaurantSchema(BaseModel):
    name: str
    address: str

@router.get("/")
def list_restaurants(request):
    # Your logic to list restaurants
    return {"restaurants": []}

@router.post("/")
def create_restaurant(request, restaurant: RestaurantSchema):
    # Your logic to create a restaurant
    return {"message": "Restaurant created", "restaurant": restaurant}
