from typing import List
from django.shortcuts import get_object_or_404
from restaurant.models.restaurant import Restaurant
from restaurant_customer.models import RestaurantCustomer


class RestaurantCustomerService:
    @staticmethod
    def create_customer(restaurant_id: str, customer_data: dict) -> dict:
        restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)

        customer = RestaurantCustomer.objects.create(
            restaurant=restaurant,
            **customer_data
        )

        return {
            "restaurant_customer_id": str(customer.restaurant_customer_id),
            **customer_data
        }

    @staticmethod
    def get_restaurant_customers(restaurant_id: str) -> List[dict]:
        restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
        return [
            {
                "restaurant_customer_id": str(customer.restaurant_customer_id),
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "email": customer.email,
                "country_code": customer.country_code,
                "phone": customer.phone,
                "birthday": customer.birthday
            }
            for customer in restaurant.customers.all()
        ]