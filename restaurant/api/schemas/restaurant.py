from ninja import Schema
from unit.api.schemas.schedule import WorkingHoursSchema, BlockedHoursSchema
from unit.api.schemas.unit import UnitResponseSchema
from typing import List, Optional
from datetime import datetime, time
from uuid import UUID
from pydantic import EmailStr, AnyUrl


class AddressSchema(Schema):
    address_id: UUID
    cep: str
    street: str
    number: str
    neighborhood: str
    city: str
    state: str
    country: str
    complement: str = None
    maps_url: Optional[AnyUrl] = None


class RestaurantCreateSchema(Schema):
    name: str
    cnpj: str
    category_id: UUID
    cuisine_type_ids: List[UUID]
    country_code: str
    phone: str
    email: EmailStr
    website: Optional[AnyUrl] = None
    description: Optional[str] = None
    image: Optional[AnyUrl] = None
    addresses: List[AddressSchema]


class RestaurantResponseSchema(Schema):
    restaurant_id: UUID
    name: str
    cnpj: str
    category: Optional[str]
    cuisine_types: List[str]
    units: List[UnitResponseSchema]
