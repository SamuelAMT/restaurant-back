from typing import List
from django.db import transaction
from django.core.exceptions import ValidationError
from ..models.restaurant import Restaurant, RestaurantCategory, CuisineType
from unit.services.unit_service import UnitService

class RestaurantService:
    @staticmethod
    def get_restaurants() -> List[Restaurant]:
        """
        Retrieve all restaurants with their related data.
        """
        return (Restaurant.objects
            .select_related('category')
            .prefetch_related(
                'cuisine_types',
                'units',
                'units__working_hours',
                'units__blocked_hours'
            )
            .all()
            .order_by('name'))
    
    @staticmethod
    @transaction.atomic
    def create_restaurant(
        name: str,
        cnpj: str,
        admin_user,
        category_id: str,
        cuisine_type_ids: List[str],
        address_data: dict = None,
        **kwargs
    ) -> Restaurant:
        """
        Create a restaurant with its main unit.
        """
        category = RestaurantCategory.objects.get(pk=category_id)
        
        restaurant = Restaurant.objects.create(
            name=name,
            cnpj=cnpj,
            admin=admin_user,
            category=category,
            **kwargs
        )
        
        cuisine_types = CuisineType.objects.filter(cuisine_id__in=cuisine_type_ids)
        restaurant.cuisine_types.set(cuisine_types)

        if address_data:
            UnitService.create_unit(
                restaurant=restaurant,
                name=f"{name} - Main Unit",
                address_data=address_data,
                is_main_unit=True
            )
        
        return restaurant

    @staticmethod
    def validate_restaurant_unit(restaurant_id: str, unit_id: str) -> bool:
        """
        Validate if a unit belongs to a restaurant.
        """
        return Restaurant.objects.filter(
            restaurant_id=restaurant_id,
            units__unit_id=unit_id
        ).exists()