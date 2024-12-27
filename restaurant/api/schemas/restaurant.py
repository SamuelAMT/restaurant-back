from ninja import Schema
from typing import List, Optional
from datetime import datetime, time
from uuid import UUID
from pydantic import EmailStr, AnyUrl

class WorkingHoursSchema(Schema):
    day_of_week: int
    opening_time: time
    closing_time: time
    is_closed: bool = False

class BlockedHoursSchema(Schema):
    start_datetime: datetime
    end_datetime: datetime
    reason: Optional[str] = None

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

class RestaurantResponseSchema(Schema):
    restaurant_id: UUID
    name: str
    cnpj: str
    category: str
    cuisine_types: List[str]
    units: List[RestaurantUnitSchema]