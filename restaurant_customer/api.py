from ninja import Router, Schema
from typing import Optional
from restaurant_customer.models import RestaurantCustomer

restaurant_customer_router = Router()

class CustomerSchema(Schema):
    name: str
    lastname: str
    email: str
    phone: str
    birthday: Optional[str] = None

@restaurant_customer_router.get("/{customer_id}", response=CustomerSchema)
def get_customer(request, customer_id: str):
    try:
        customer = RestaurantCustomer.objects.get(id=customer_id)
        return customer
    except RestaurantCustomer.DoesNotExist:
        return {"error": "Customer not found"}, 404

@restaurant_customer_router.post("/customers/", response=CustomerSchema)
def create_customer(request, payload: CustomerSchema):
    customer = RestaurantCustomer.objects.create(
        name=payload.name,
        lastname=payload.lastname,
        email=payload.email,
        phone=payload.phone,
        birthday=payload.birthday,
    )
    return customer