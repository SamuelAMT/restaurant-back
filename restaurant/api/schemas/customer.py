from ninja import Schema
from datetime import date
from typing import Optional
from pydantic import EmailStr

class CustomerCreateSchema(Schema):
    first_name: str
    last_name: str
    email: EmailStr
    country_code: str
    phone: str
    birthday: Optional[date] = None

class CustomerResponseSchema(CustomerCreateSchema):
    customer_id: str