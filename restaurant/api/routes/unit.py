from ninja import Router
from django.http import HttpRequest
from datetime import datetime
from typing import List
from ...services.restaurant_service import RestaurantService
from ..schemas.unit import UnitCreateSchema, UnitResponseSchema
from ..schemas.schedule import (
    WorkingHoursSchema,
    BlockedHoursSchema,
    WorkingHoursResponseSchema,
    BlockedHoursResponseSchema
)

unit_router = Router()

@unit_router.post("/{restaurant_id}/units", response=UnitResponseSchema)
def add_unit(request: HttpRequest, restaurant_id: str, payload: UnitCreateSchema):
    unit = RestaurantService.add_restaurant_unit(
        restaurant_id=restaurant_id,
        unit_name=payload.name,
        is_main_unit=payload.is_main_unit
    )
    return {
        "unit_id": unit.unit_id,
        "name": unit.name,
        "is_main_unit": unit.is_main_unit,
        "working_hours": [],
        "blocked_hours": []
    }

@unit_router.post("/{restaurant_id}/units/{unit_id}/working-hours", response=List[WorkingHoursResponseSchema])
def set_working_hours(
    request: HttpRequest,
    restaurant_id: str,
    unit_id: str,
    working_hours: List[WorkingHoursSchema]
):
    hours = RestaurantService.set_working_hours(
        unit_id=unit_id,
        working_hours=[hours.dict() for hours in working_hours]
    )
    return [
        {
            "working_hours_id": wh.working_hours_id,
            "day_of_week": wh.day_of_week,
            "opening_time": wh.opening_time,
            "closing_time": wh.closing_time,
            "is_closed": wh.is_closed
        }
        for wh in hours
    ]

@unit_router.post("/{restaurant_id}/units/{unit_id}/blocked-hours", response=BlockedHoursResponseSchema)
def add_blocked_hours(
    request: HttpRequest,
    restaurant_id: str,
    unit_id: str,
    payload: BlockedHoursSchema
):
    blocked_hours = RestaurantService.add_blocked_hours(
        unit_id=unit_id,
        start_datetime=payload.start_datetime,
        end_datetime=payload.end_datetime,
        reason=payload.reason
    )
    return {
        "blocked_hours_id": blocked_hours.blocked_hours_id,
        "start_datetime": blocked_hours.start_datetime,
        "end_datetime": blocked_hours.end_datetime,
        "reason": blocked_hours.reason
    }

@unit_router.get("/{restaurant_id}/units/{unit_id}/availability")
def check_availability(
    request: HttpRequest,
    restaurant_id: str,
    unit_id: str,
    check_datetime: datetime
):
    is_available = RestaurantService.is_unit_available(
        unit_id=unit_id,
        check_datetime=check_datetime
    )
    return {"is_available": is_available}