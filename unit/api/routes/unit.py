from ninja import Router
from django.http import HttpRequest
from datetime import datetime
from typing import List
from unit.services.unit_service import UnitService
from ..schemas.unit import (
    UnitCreateSchema,
    UnitResponseSchema,
)
from ..schemas.schedule import (
    WorkingHoursSchema,
    BlockedHoursSchema,
    WorkingHoursResponseSchema,
    BlockedHoursResponseSchema
)

unit_router = Router()

@unit_router.post("/{restaurant_id}/units", response=UnitResponseSchema)
def create_unit(request: HttpRequest, restaurant_id: str, payload: UnitCreateSchema):
    return UnitService.create_unit(restaurant_id, payload)

@unit_router.post("/{restaurant_id}/units/{unit_id}/working-hours", response=List[WorkingHoursResponseSchema])
def set_working_hours(request: HttpRequest, restaurant_id: str, unit_id: str, working_hours: List[WorkingHoursSchema]):
    return UnitService.set_working_hours(unit_id, working_hours)

@unit_router.post("/{restaurant_id}/units/{unit_id}/blocked-hours", response=BlockedHoursResponseSchema)
def add_blocked_hours(request: HttpRequest, restaurant_id: str, unit_id: str, payload: BlockedHoursSchema):
    return UnitService.add_blocked_hours(unit_id, payload)

@unit_router.get("/{restaurant_id}/units/{unit_id}/availability")
def check_availability(request: HttpRequest, restaurant_id: str, unit_id: str, check_datetime: datetime):
    return {"is_available": UnitService.is_available(unit_id, check_datetime)}