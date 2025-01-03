from ninja import Schema
from datetime import datetime
from typing import Optional

class AddressIn(Schema):
    cep: str
    street: str
    number: str
    neighborhood: str
    city: str
    state: str
    country: str
    complement: Optional[str] = None

class AddressOut(AddressIn):
    address_id: int
    created_at: datetime
    updated_at: datetime