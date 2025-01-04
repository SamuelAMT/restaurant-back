from ninja import Schema
from datetime import datetime
from uuid import UUID
from typing import Optional

class AddressBase(Schema):
    cep: str
    street: str
    number: str
    neighborhood: str
    city: str
    state: str
    country: str
    complement: Optional[str] = None
    maps_url: Optional[str] = None
    unit_id: Optional[UUID] = None

class AddressIn(Schema):
    pass

class AddressOut(AddressIn):
    address_id: UUID
    created_at: datetime
    updated_at: datetime