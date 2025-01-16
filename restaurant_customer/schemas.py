from ninja import Schema
from uuid import UUID
from typing import List, Optional
from pydantic import EmailStr
from datetime import date


class RestaurantCustomerCreateSchema(Schema):
    first_name: str
    last_name: str
    email: EmailStr
    country_code: str
    phone: str
    birthday: Optional[date] = None

class RestaurantCustomerResponseSchema(RestaurantCustomerCreateSchema):
    restaurant_customer_id: str

class RestaurantCustomerSchema(Schema):
    restaurant_customer_id: Optional[str] = None
    first_name: str
    last_name: str
    email: EmailStr
    country_code: Optional[str] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None