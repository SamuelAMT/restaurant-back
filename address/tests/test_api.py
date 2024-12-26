from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from ..models import Address
from restaurant.models import Restaurant
from custom_auth.models import CustomUser

class AddressAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            email="test@example.com"
        )
        self.user = CustomUser.objects.create_user(
            email="test@example.com",
            password="testpass123",
            restaurant=self.restaurant
        )
        self.client.force_authenticate(user=self.user)

    def test_create_address(self):
        data = {
            "cep": "12345-678",
            "street": "Test Street",
            "number": "123",
            "neighborhood": "Test Neighborhood",
            "city": "Test City",
            "state": "ST",
            "country": "Test Country"
        }
        response = self.client.post(reverse('api:v1:address-create'), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Address.objects.count(), 1)