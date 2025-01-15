from uuid import UUID
from typing import List
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Address
from .schemas import AddressIn
from custom_auth.models import Role

User = get_user_model()

class AddressService:
    @staticmethod
    def get_restaurant_addresses(user) -> List[Address]:
        """
        Get all addresses based on the user's role:
        - SUPERADMIN: All addresses.
        - RESTAURANT_ADMIN: All addresses for their restaurant.
        - RESTAURANT_SUB_ADMIN: All addresses for their restaurant.
        - RESTAURANT_STAFF: Addresses for their specific unit.
        """
        if user.role == Role.SUPERADMIN:
            # Superadmin can see all addresses
            return Address.objects.all()
        elif user.role in [Role.RESTAURANT_ADMIN, Role.RESTAURANT_SUB_ADMIN]:
            # Restaurant Admin and Sub Admin can see all addresses for their restaurant
            if hasattr(user, 'restaurant'):
                return Address.objects.filter(unit__restaurant=user.restaurant)
            else:
                return Address.objects.none()  # No restaurant associated
        elif user.role == Role.RESTAURANT_STAFF:
            # Restaurant Staff can see addresses for their specific unit
            if hasattr(user, 'unit'):
                return Address.objects.filter(unit=user.unit)
            else:
                return Address.objects.none()
        else:
            # Default: No addresses for other roles
            return Address.objects.none()

    @staticmethod
    def create_address(user, address_data: AddressIn) -> Address:
        """Create a new address for a unit"""
        if hasattr(user, 'unit'):
            unit = user.unit
        elif hasattr(user, 'restaurant'):
            unit = user.restaurant.units.filter(is_main_unit=True).first()
            if not unit:
                raise ValueError("No main unit found for this restaurant")
        else:
            raise ValueError("User must be associated with a restaurant or unit")

        address = Address.objects.create(
            unit=unit,
            **address_data.dict()
        )
        return address

    @staticmethod
    def update_address(address_id: UUID, address_data: AddressIn) -> Address:
        """Update an existing address"""
        address = get_object_or_404(Address, address_id=address_id)
        for key, value in address_data.dict().items():
            setattr(address, key, value)
        address.save()
        return address

    @staticmethod
    def delete_address(address_id: UUID) -> None:
        """Delete an address"""
        address = get_object_or_404(Address, address_id=address_id)
        address.delete()