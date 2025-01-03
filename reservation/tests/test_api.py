from django.test import TestCase, Client
from django.urls import reverse
from restaurant.models import Restaurant
from ..models import Reservation
from datetime import datetime, time

class ReservationAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            restaurant_id="550e8400-e29b-41d4-a716-446655440000"
        )
        self.valid_payload = {
            "reserver": "John Doe",
            "amount_of_people": 2,
            "amount_of_hours": 2,
            "start_time": "18:00:00",
            "end_time": "20:00:00",
            "reservation_date": "2024-12-31",
            "email": "john@example.com",
            "country_code": "US",
            "phone": "1234567890",
        }

    def test_create_reservation_success(self):
        response = self.client.post(
            reverse('api-1.0.0:reservation:create_reservation', 
                   kwargs={'restaurant_id': self.restaurant.restaurant_id}),
            self.valid_payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('reservation_hash', response.json())
        self.assertIn('status', response.json())
        self.assertEqual(response.json()['status'], 'confirmed')

    def test_create_reservation_invalid_data(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload['amount_of_people'] = 0

        response = self.client.post(
            reverse('api-1.0.0:reservation:create_reservation', 
                   kwargs={'restaurant_id': self.restaurant.restaurant_id}),
            invalid_payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 422)