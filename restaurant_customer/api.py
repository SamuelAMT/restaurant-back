from ninja import Router, Schema
from datetime import date
from typing import Optional
from pydantic import EmailStr
from restaurant_customer.models import RestaurantCustomer

restaurant_customer_router = Router()

class CustomerSchema(Schema):
    name: str
    lastname: str
    email: EmailStr
    country_code: str
    phone: str
    birthday: Optional[date] = None

@restaurant_customer_router.get("/{restaurant_customer_id}", response=CustomerSchema)
def get_customer(request, restaurant_customer_id: str):
    try:
        customer = RestaurantCustomer.objects.get(id=restaurant_customer_id)
        return customer
    except RestaurantCustomer.DoesNotExist:
        return {"error": "Customer not found"}, 404

@restaurant_customer_router.post("/customers/", response=CustomerSchema)
def create_customer(request, payload: CustomerSchema):
    customer = RestaurantCustomer.objects.create(
        name=payload.name,
        lastname=payload.lastname,
        email=payload.email,
        country_code=payload.country_code,
        phone=payload.phone,
        birthday=payload.birthday,
    )
    return customer