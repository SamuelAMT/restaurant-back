from typing import List, Dict, Optional, Any
from uuid import UUID
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404
from ..models import Reservation
from restaurant.models import Restaurant
from restaurant_customer.models import RestaurantCustomer
from .constants import ReservationStatus

class ReservationService:
    DEFAULT_PAGE_SIZE = 10
    
    @staticmethod
    def create_reservation(restaurant_id: str, reservation_data: dict) -> Reservation:
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
    
    @staticmethod
    def get_reservations(
        restaurant_id: str,
        unit_id: UUID,
        page: int = 1,
        page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
        reservations = Reservation.objects.filter(restaurant=restaurant)
        
        if unit_id:
            reservations = reservations.filter(unit_id=unit_id)
        
        reservations = reservations.order_by('-reservation_date', '-start_time')
        
        paginator = Paginator(reservations, page_size or ReservationService.DEFAULT_PAGE_SIZE)
        
        try:
            page_obj = paginator.page(page)
        except EmptyPage:
            # If page is out of range, deliver last page
            page_obj = paginator.page(paginator.num_pages)
        
        results = [
            {
                "reservation_hash": str(res.reservation_hash),
                "reserver": res.reserver,
                "email": res.email,
                "phone": res.phone,
                "amount_of_people": res.amount_of_people,
                "amount_of_hours": res.amount_of_hours,
                "start_time": res.start_time,
                "end_time": res.end_time,
                "reservation_date": res.reservation_date,
                "status": res.status,
                "customer_name": f"{res.customer.first_name} {res.customer.last_name}" if res.customer else None,
                "unit_id": res.unit_id if hasattr(res, 'unit_id') else None
            }
            for res in page_obj.object_list
        ]
        
        return {
            "count": paginator.count,
            "next_page": page + 1 if page_obj.has_next() else None,
            "previous_page": page - 1 if page_obj.has_previous() else None,
            "results": results
        }