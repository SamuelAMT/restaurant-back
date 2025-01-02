from ninja import Schema
from typing import List
from uuid import UUID
from .schedule import WorkingHoursResponseSchema, BlockedHoursResponseSchema

class UnitCreateSchema(Schema):
    name: str
    is_main_unit: bool = False

class UnitResponseSchema(Schema):
    unit_id: UUID
    name: str
    is_main_unit: bool
    working_hours: List[WorkingHoursResponseSchema]
    blocked_hours: List[BlockedHoursResponseSchema]