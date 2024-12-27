from django.shortcuts import get_object_or_404
from ..models import Reservation
from restaurant.models import Restaurant
from restaurant_customer.models import RestaurantCustomer
from .constants import ReservationStatus

class ReservationService:
    @staticmethod
    def create_reservation(restaurant_id: str, reservation_data: dict) -> Reservation:  # Note return type
        restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
        
        customer, _ = RestaurantCustomer.objects.get_or_create(
            email=reservation_data.email,
            defaults={
                'name': reservation_data.reserver,
                'lastname': '',
                'country_code': reservation_data.country_code,
                'phone': reservation_data.phone,
                'birthday': reservation_data.birthday,
            }
        )

        reservation_dict = reservation_data.dict()

        reservation = Reservation.objects.create(
            restaurant=restaurant,
            customer=customer,
            **reservation_dict
        )

        return reservation