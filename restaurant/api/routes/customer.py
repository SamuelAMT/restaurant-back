from ninja import Router
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from restaurant_customer.services import RestaurantCustomerService
from restaurant_customer.schemas import RestaurantCustomerCreateSchema, RestaurantCustomerResponseSchema

customer_router = Router()

@customer_router.post("/{restaurant_id}/customers", response=RestaurantCustomerResponseSchema)
def create_customer(request: HttpRequest, restaurant_id: str, payload: RestaurantCustomerCreateSchema):
    customer = RestaurantCustomerService.create_customer(restaurant_id, payload)
    return customer

@customer_router.get("/{restaurant_id}/customers", response=list[RestaurantCustomerResponseSchema])
def list_customers(request: HttpRequest, restaurant_id: str):
    return RestaurantCustomerService.get_restaurant_customers(restaurant_id)
