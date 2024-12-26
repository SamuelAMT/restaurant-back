from typing import List
from django.contrib.auth import get_user_model
from .models import Address
from .schemas import AddressIn

User = get_user_model()

class AddressService:
    @staticmethod
    def get_restaurant_addresses(user) -> List[Address]:
        """Get all addresses for a restaurant"""
        return Address.objects.filter(restaurant=user.restaurant)

    @staticmethod
    def create_address(user, address_data: AddressIn) -> Address:
        """Create a new address"""
        address = Address.objects.create(
            restaurant=user.restaurant,
            **address_data.dict()
        )
        return address

    @staticmethod
    def update_address(address_id: int, address_data: AddressIn) -> Address:
        """Update an existing address"""
        address = Address.objects.get(address_id=address_id)
        for key, value in address_data.dict().items():
            setattr(address, key, value)
        address.save()
        return address

    @staticmethod
    def delete_address(address_id: int) -> None:
        """Delete an address"""
        Address.objects.filter(address_id=address_id).delete()
