from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import Address
from restaurant.models import Restaurant

class AddressTests(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            email="test@example.com"
        )

    def test_create_address(self):
        address = Address.objects.create(
            restaurant=self.restaurant,
            cep="12345-678",
            street="Test Street",
            number="123",
            neighborhood="Test Neighborhood",
            city="Test City",
            state="ST",
            country="Test Country"
        )
        self.assertIsNotNull(address.address_id)
        self.assertEqual(address.cep, "12345678")

    def test_invalid_cep(self):
        with self.assertRaises(ValidationError):
            Address.objects.create(
                restaurant=self.restaurant,
                cep="invalid-cep",
                street="Test Street",
                number="123",
                neighborhood="Test Neighborhood",
                city="Test City",
                state="ST",
                country="Test Country"
            )