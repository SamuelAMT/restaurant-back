from ninja import Router
from uuid import UUID
from typing import List
from django.shortcuts import get_object_or_404
from ninja.security import HttpBearer
from .schemas import AddressIn, AddressOut, AddressBase
from .models import Address
from .services import AddressService

address_router = Router()


@address_router.get("/{address_id}", response=AddressBase)
def get_address(request, address_id: UUID):
    """Get specific address details"""
    addresses = AddressService.get_restaurant_addresses(request.user)
    address = get_object_or_404(addresses, address_id=address_id)
    return address


@address_router.post("/", response=AddressOut)
def create_address(request, payload: AddressIn):
    """Create a new address"""
    try:
        address = AddressService.create_address(request.user, payload)
        return address
    except ValueError as e:
        return {"error": str(e)}, 400


@address_router.put("/{address_id}", response=AddressOut)
def update_address(request, address_id: UUID, payload: AddressIn):
    """Update an existing address"""
    addresses = AddressService.get_restaurant_addresses(request.user)
    get_object_or_404(addresses, address_id=address_id)
    address = AddressService.update_address(address_id, payload)
    return address


@address_router.delete("/{address_id}")
def delete_address(request, address_id: UUID):
    """Delete an address"""
    addresses = AddressService.get_restaurant_addresses(request.user)
    get_object_or_404(addresses, address_id=address_id)
    AddressService.delete_address(address_id)
    return {"success": True}
