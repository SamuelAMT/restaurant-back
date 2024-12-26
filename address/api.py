from ninja import Router
from typing import List
from .schemas import AddressIn, AddressOut
from .models import Address
from django.shortcuts import get_object_or_404
from .services import AddressService

address_router = Router()

@address_router.get("/", response=List[AddressOut])
def list_addresses(request):
    """List all addresses associated with the authenticated user's restaurant"""
    addresses = AddressService.get_restaurant_addresses(request.user)
    return addresses

@address_router.post("/", response=AddressOut)
def create_address(request, payload: AddressIn):
    """Create a new address for the authenticated user's restaurant"""
    address = AddressService.create_address(request.user, payload)
    return address

@address_router.get("/{address_id}", response=AddressOut)
def get_address(request, address_id: int):
    """Get specific address details"""
    address = get_object_or_404(Address, address_id=address_id)
    return address

@address_router.put("/{address_id}", response=AddressOut)
def update_address(request, address_id: int, payload: AddressIn):
    """Update an existing address"""
    address = AddressService.update_address(address_id, payload)
    return address

@address_router.delete("/{address_id}")
def delete_address(request, address_id: int):
    """Delete an address"""
    AddressService.delete_address(address_id)
    return {"success": True}