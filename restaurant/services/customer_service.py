from typing import List
from django.shortcuts import get_object_or_404
from ..models import Restaurant
from restaurant_customer.models import RestaurantCustomer

class CustomerService:
    @staticmethod
    def create_customer(restaurant_id: str, customer_data: dict) -> dict:
        restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
        
        customer = RestaurantCustomer.objects.create(**customer_data)
        restaurant.customers.add(customer)
        
        return {
            "customer_id": str(customer.customer_id),
            **customer_data
        }

    @staticmethod
    def get_restaurant_customers(restaurant_id: str) -> List[dict]:
        restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
        return [
            {
                "customer_id": str(customer.customer_id),
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "email": customer.email,
                "country_code": customer.country_code,
                "phone": customer.phone,
                "birthday": customer.birthday
            }
            for customer in restaurant.customers.all()
        ]