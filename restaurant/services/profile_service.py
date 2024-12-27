from django.shortcuts import get_object_or_404
from ..models import Restaurant

class ProfileService:
    @staticmethod
    def get_profile(restaurant_id: str):
        restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
        address = restaurant.addresses.first() if restaurant.addresses.exists() else None
        
        return {
            "name": restaurant.name,
            "email": restaurant.email or "",
            "phone": restaurant.phone or "",
            "website": restaurant.website or "",
            "description": restaurant.description or "",
            "address": (
                f"{address.street}, {address.number} - {address.neighborhood}"
                if address else "No address"
            ),
        }