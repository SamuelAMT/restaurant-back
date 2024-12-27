from ninja import Schema
from .schedule import WorkingHoursSchema, BlockedHoursSchema
from typing import List, Optional
from datetime import datetime, time
from uuid import UUID
from pydantic import EmailStr, AnyUrl


class AddressSchema(Schema):
    cep: str
    street: str
    number: str
    neighborhood: str
    city: str
    state: str
    country: str
    complement: str = None


class RestaurantUnitSchema(Schema):
    unit_id: UUID
    name: str
    is_main_unit: bool
    working_hours: List[WorkingHoursSchema]
    blocked_hours: List[BlockedHoursSchema]


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
    category: str
    cuisine_types: List[str]
    units: List[RestaurantUnitSchema]
