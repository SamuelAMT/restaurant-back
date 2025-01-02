from typing import List
from uuid import UUID
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from ..models import Restaurant
from unit.models.unit import Unit
from reservation.models import Reservation
from reservation.core.constants import ReservationStatus

class ReservationService:
    @staticmethod
    def create_reservation(restaurant_id: str, unit_id: str, reservation_data: dict) -> dict:
        restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
        unit = get_object_or_404(Unit, unit_id=unit_id, restaurant=restaurant)
        
        # Check unit availability using unit service
        if not unit.is_available(reservation_data['reservation_date']):
            raise ValidationError("Unit is not available at the specified time")
            
        reservation = Reservation.objects.create(
            restaurant=restaurant,
            unit=unit,
            **reservation_data
        )
        
        return {
            "reservation_hash": str(reservation.reservation_hash),
            **reservation_data,
            "amount_of_hours": reservation.amount_of_hours,
            "status": reservation.status,
            "unit_name": unit.name  # Add unit information
        }

    @staticmethod
    def get_reservations(restaurant_id: str, unit_id: str = None) -> List[dict]:
        restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
        reservations = Reservation.objects.filter(restaurant=restaurant)
        
        if unit_id:
            reservations = reservations.filter(unit_id=unit_id)
            
        return [
            {
                "reservation_hash": str(res.reservation_hash),
                "reserver": res.reserver,
                "amount_of_people": res.amount_of_people,
                "amount_of_hours": res.amount_of_hours,
                "start_time": res.start_time,
                "end_time": res.end_time,
                "reservation_date": res.reservation_date,
                "status": res.status,
                "unit_name": res.unit.name,  # Add unit information
                "customer_name": f"{res.customer.first_name} {res.customer.last_name}" if res.customer else None
            }
            for res in reservations
        ]

    @staticmethod
    def cancel_reservation(restaurant_id: str, reservation_hash: str) -> dict:
        restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
        reservation = get_object_or_404(
            Reservation,
            reservation_hash=reservation_hash,
            restaurant=restaurant
        )
        
        reservation.status = ReservationStatus.CANCELED
        reservation.save()
        
        return {"status": "success", "message": "Reservation cancelled successfully"}