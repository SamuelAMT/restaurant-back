from django.shortcuts import get_object_or_404
from ..models import Restaurant
from reservation.models import Reservation

class DashboardService:
    @staticmethod
    def get_dashboard_data(restaurant_id: str):
        restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
        total_reservations = Reservation.objects.filter(restaurant=restaurant).count()
        total_customers = restaurant.customers.count()
        canceled_reservations = Reservation.objects.filter(
            restaurant=restaurant, status="canceled").count()
        new_customers = 0  # Frontend should filter by date
        new_reservations = Reservation.objects.filter(
            restaurant=restaurant, status="confirmed").count()

        return {
            "total_reservations": total_reservations,
            "new_customers": new_customers,
            "new_reservations": new_reservations,
            "total_customers": total_customers,
            "canceled_reservations": canceled_reservations,
        }