from ninja import Router
from restaurant.models import Restaurant
router = Router()

@router.get("/restaurants")
def get_restaurants(request):
    restaurants = Restaurant.objects.all()
    return [{"id": r.id, "name": r.name} for r in restaurants]
