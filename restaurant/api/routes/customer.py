from ninja import Router
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ...services.customer_service import CustomerService
from ..schemas.customer import CustomerCreateSchema, CustomerResponseSchema

customer_router = Router()

@customer_router.post("/{restaurant_id}/customers", response=CustomerResponseSchema)
def create_customer(request: HttpRequest, restaurant_id: str, payload: CustomerCreateSchema):
    customer = CustomerService.create_customer(restaurant_id, payload)
    return customer

@customer_router.get("/{restaurant_id}/customers", response=list[CustomerResponseSchema])
def list_customers(request: HttpRequest, restaurant_id: str):
    return CustomerService.get_restaurant_customers(restaurant_id)  
