from ninja import Schema
from unit.api.schemas.schedule import WorkingHoursSchema, BlockedHoursSchema
from unit.api.schemas.unit import UnitResponseSchema
from typing import List, Optional
from datetime import datetime, time
from uuid import UUID
from pydantic import EmailStr, AnyUrl, field_validator


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
    country_code: str
    phone: str
    email: EmailStr
    website: Optional[str]
    description: Optional[str]
    image: Optional[str]
    role: str
    addresses: List[AddressSchema]
    units: List[UnitResponseSchema]

    @field_validator("website", "image", mode="before")
    def convert_url_to_string(cls, value):
        if value is not None:
            return str(value)
        return value
