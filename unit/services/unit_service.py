from typing import List, Optional
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from ..models.unit import Unit
from reservation.models import Reservation
from reservation.core.constants import ReservationStatus
from address.models import Address
from unit.models.schedule import WorkingHours, BlockedHours
from restaurant.models import Restaurant

class UnitService:
    @staticmethod
    def create_unit(
        restaurant: Restaurant,
        name: str,
        address_data: dict,
        is_main_unit: bool = False
    ) -> Unit:
        """
        Create a new unit for a restaurant.
        """
        # Check if trying to create a main unit when one already exists
        if is_main_unit and restaurant.units.filter(is_main_unit=True).exists():
            raise ValidationError("Restaurant already has a main unit")

        address = Address.objects.create(**address_data)
        
        unit = Unit.objects.create(
            restaurant=restaurant,
            name=name,
            is_main_unit=is_main_unit,
            address=address
        )
        
        return unit

    @staticmethod
    def set_working_hours(unit_id: str, working_hours: List[dict]) -> List[WorkingHours]:
        """
        Set working hours for a unit, replacing any existing ones.
        """
        unit = get_object_or_404(Unit, unit_id=unit_id)
        
        # Clear existing working hours
        unit.working_hours.all().delete()
        
        # Create new working hours
        created_hours = []
        for hours in working_hours:
            wh = WorkingHours.objects.create(
                unit=unit,
                day_of_week=hours['day_of_week'],
                opening_time=hours['opening_time'],
                closing_time=hours['closing_time'],
                is_closed=hours.get('is_closed', False)
            )
            created_hours.append(wh)
        
        return created_hours

    @staticmethod
    def add_blocked_hours(
        unit_id: str,
        start_datetime: datetime,
        end_datetime: datetime,
        reason: Optional[str] = None
    ) -> BlockedHours:
        """
        Add blocked hours for a unit.
        """
        unit = get_object_or_404(Unit, unit_id=unit_id)
        
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
    def is_available(unit_id: str, check_datetime: datetime) -> bool:
        """
        Check if a unit is available at a specific datetime.
        """
        unit = get_object_or_404(Unit, unit_id=unit_id)
        
        # Check blocked hours
        if unit.blocked_hours.filter(
            start_datetime__lte=check_datetime,
            end_datetime__gte=check_datetime
        ).exists():
            return False
        
        # Check working hours
        day_of_week = check_datetime.weekday()
        time = check_datetime.time()
        
        try:
            working_hours = unit.working_hours.get(day_of_week=day_of_week)
            if working_hours.is_closed:
                return False
            return working_hours.opening_time <= time <= working_hours.closing_time
        except WorkingHours.DoesNotExist:
            return False

    @staticmethod
    def get_unit_schedule(unit_id: str) -> dict:
        """
        Get the complete schedule information for a unit.
        """
        unit = get_object_or_404(Unit, unit_id=unit_id)
        return {
            'working_hours': list(unit.working_hours.all()),
            'blocked_hours': list(unit.blocked_hours.all())
        }