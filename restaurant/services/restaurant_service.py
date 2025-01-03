from typing import List, Optional
from django.db import transaction
from django.core.exceptions import ValidationError
from ..models.restaurant import Restaurant, RestaurantCategory, CuisineType
from ..models.unit import RestaurantUnit
from ..models.schedule import WorkingHours, BlockedHours
from datetime import datetime, time

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
        **kwargs
    ) -> Restaurant:
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

        RestaurantUnit.objects.create(
            restaurant=restaurant,
            name=f"{name} - Main Unit",
            is_main_unit=True
        )
        
        return restaurant

    @staticmethod
    def add_restaurant_unit(
        restaurant_id: str,
        unit_name: str,
        is_main_unit: bool = False
    ) -> RestaurantUnit:
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        
        if is_main_unit and restaurant.units.filter(is_main_unit=True).exists():
            raise ValidationError("Restaurant already has a main unit")
        
        return RestaurantUnit.objects.create(
            restaurant=restaurant,
            name=unit_name,
            is_main_unit=is_main_unit
        )

    @staticmethod
    def set_working_hours(
        unit_id: str,
        working_hours: List[dict]
    ) -> List[WorkingHours]:
        unit = RestaurantUnit.objects.get(pk=unit_id)
        
        unit.working_hours.all().delete()
        
        created_hours = []
        for hours in working_hours:
            created_hours.append(WorkingHours.objects.create(
                unit=unit,
                day_of_week=hours['day_of_week'],
                opening_time=hours['opening_time'],
                closing_time=hours['closing_time'],
                is_closed=hours.get('is_closed', False)
            ))
        
        return created_hours

    @staticmethod
    def add_blocked_hours(
        unit_id: str,
        start_datetime: datetime,
        end_datetime: datetime,
        reason: Optional[str] = None
    ) -> BlockedHours:
        unit = RestaurantUnit.objects.get(pk=unit_id)
        
        if start_datetime >= end_datetime:
            raise ValidationError("End datetime must be after start datetime")
        
        # Check for overlapping blocked hours
        if unit.blocked_hours.filter(
            start_datetime__lt=end_datetime,
            end_datetime__gt=start_datetime
        ).exists():
            raise ValidationError("Overlapping blocked hours exist")
        
        return BlockedHours.objects.create(
            unit=unit,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            reason=reason
        )

    @staticmethod
    def is_unit_available(
        unit_id: str,
        check_datetime: datetime
    ) -> bool:
        unit = RestaurantUnit.objects.get(pk=unit_id)
        
        if unit.blocked_hours.filter(
            start_datetime__lte=check_datetime,
            end_datetime__gte=check_datetime
        ).exists():
            return False
        
        day_of_week = check_datetime.weekday()
        check_time = check_datetime.time()
        
        try:
            working_hours = unit.working_hours.get(day_of_week=day_of_week)
            if working_hours.is_closed:
                return False
            return working_hours.opening_time <= check_time <= working_hours.closing_time
        except WorkingHours.DoesNotExist:
            return False