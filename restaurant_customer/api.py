from ninja import Router, Schema
from restaurant_customer.models import RestaurantCustomer

restaurant_customer_router = Router()


class CustomerSchema(Schema):
    id: str
    name: str
    lastname: str
    email: str
    phone: str


@restaurant_customer_router.get("/{customer_id}", response=CustomerSchema)
def get_customer(request, customer_id: str):
    try:
        customer = RestaurantCustomer.objects.get(id=customer_id)
        return customer
    except RestaurantCustomer.DoesNotExist:
        return {"error": "Customer not found"}, 404
