from django.test import TestCase
from django.utils import timezone
from ..models import Reservation
from restaurant.models import Restaurant
from restaurant_customer.models import RestaurantCustomer

class ReservationModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name="Test Restaurant")
        self.customer = RestaurantCustomer.objects.create(
            email="test@example.com",
            name="Test Customer"
        )

    def test_create_reservation(self):
        reservation = Reservation.objects.create(
            reserver="Test User",
            amount_of_people=2,
            amount_of_hours=2,
            start_time=timezone.now().time(),
            end_time=timezone.now().time(),
            reservation_date=timezone.now().date(),
            email="test@example.com",
            restaurant=self.restaurant,
            customer=self.customer
        )
        self.assertIsNotNone(reservation.reservation_hash)