from django.test import TestCase
from django.core.exceptions import ValidationError
from restaurant.models import Restaurant
from restaurant_customer.models import RestaurantCustomer
from ..core.services import ReservationService
from ..core.constants import ReservationStatus
from datetime import datetime, timedelta

class ReservationServiceTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            restaurant_id="550e8400-e29b-41d4-a716-446655440000"
        )
        self.valid_data = {
            "reserver": "John Doe",
            "amount_of_people": 2,
            "amount_of_hours": 2,
            "start_time": datetime.now().time(),
            "end_time": (datetime.now() + timedelta(hours=2)).time(),
            "reservation_date": datetime.now().date() + timedelta(days=1),
            "email": "john@example.com",
            "country_code": "US",
            "phone": "1234567890",
        }

    def test_create_reservation_success(self):
        reservation = ReservationService.create_reservation(
            self.restaurant.restaurant_id,
            self.valid_data
        )
        self.assertIsNotNone(reservation.reservation_hash)
        self.assertEqual(reservation.status, ReservationStatus.CONFIRMED)
        self.assertEqual(reservation.amount_of_people, 2)

    def test_create_reservation_creates_customer(self):
        reservation = ReservationService.create_reservation(
            self.restaurant.restaurant_id,
            self.valid_data
        )
        self.assertIsNotNone(reservation.customer)
        self.assertEqual(reservation.customer.email, "john@example.com")

    def test_create_reservation_invalid_time(self):
        invalid_data = self.valid_data.copy()
        invalid_data['start_time'] = datetime.now().time()
        invalid_data['end_time'] = datetime.now().time()
        
        with self.assertRaises(ValidationError):
            ReservationService.create_reservation(
                self.restaurant.restaurant_id,
                invalid_data
            )