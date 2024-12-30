from ninja import Router
from django.http import HttpRequest
from typing import List
from datetime import datetime
from django.shortcuts import get_object_or_404
from ...services.restaurant_service import RestaurantService
from ..schemas.restaurant import (
    RestaurantCreateSchema,
    RestaurantResponseSchema,
    WorkingHoursSchema,
    BlockedHoursSchema,
)
from ...models.restaurant import Restaurant

restaurant_router = Router()


@restaurant_router.get("/", response=List[RestaurantResponseSchema])
def list_restaurants(request: HttpRequest):
    restaurants = RestaurantService.get_restaurants()
    return [_format_restaurant_response(restaurant) for restaurant in restaurants]

def _format_restaurant_response(restaurant: Restaurant) -> RestaurantResponseSchema:
    return RestaurantResponseSchema(
        restaurant_id=restaurant.restaurant_id,
        name=restaurant.name,
        cnpj=restaurant.cnpj,
        category=restaurant.category.name if restaurant.category else None,  # Add null check here
        cuisine_types=[ct.name for ct in restaurant.cuisine_types.all()],
        units=[
            {
                "unit_id": unit.unit_id,
                "name": unit.name,
                "is_main_unit": unit.is_main_unit,
                "working_hours": [
                    {
                        "day_of_week": wh.day_of_week,
                        "opening_time": wh.opening_time,
                        "closing_time": wh.closing_time,
                        "is_closed": wh.is_closed,
                    }
                    for wh in unit.working_hours.all()
                ],
                "blocked_hours": [
                    {
                        "start_datetime": bh.start_datetime,
                        "end_datetime": bh.end_datetime,
                        "reason": bh.reason,
                    }
                    for bh in unit.blocked_hours.all()
                ],
            }
            for unit in restaurant.units.all()
        ],
    )


@restaurant_router.post("/", response=RestaurantResponseSchema)
def create_restaurant(request: HttpRequest, payload: RestaurantCreateSchema):
    restaurant = RestaurantService.create_restaurant(
        name=payload.name,
        cnpj=payload.cnpj,
        admin_user=request.user,
        category_id=payload.category_id,
        cuisine_type_ids=payload.cuisine_type_ids,
        country_code=payload.country_code,
        phone=payload.phone,
        email=payload.email,
        website=payload.website,
        description=payload.description,
        image=payload.image,
    )
    return _format_restaurant_response(restaurant)


@restaurant_router.post("/{restaurant_id}/units")
def add_unit(request: HttpRequest, restaurant_id: str, name: str):
    unit = RestaurantService.add_restaurant_unit(restaurant_id, name)
    return {"unit_id": unit.unit_id, "name": unit.name}


@restaurant_router.post("/{restaurant_id}/units/{unit_id}/working-hours")
def set_working_hours(
    request: HttpRequest,
    restaurant_id: str,
    unit_id: str,
    working_hours: List[WorkingHoursSchema],
):
    hours = RestaurantService.set_working_hours(unit_id, working_hours)
    return {"status": "success", "count": len(hours)}


@restaurant_router.post("/{restaurant_id}/units/{unit_id}/blocked-hours")
def add_blocked_hours(
    request: HttpRequest, restaurant_id: str, unit_id: str, payload: BlockedHoursSchema
):
    blocked_hours = RestaurantService.add_blocked_hours(
        unit_id, payload.start_datetime, payload.end_datetime, payload.reason
    )
    return {
        "blocked_hours_id": blocked_hours.blocked_hours_id,
        "start_datetime": blocked_hours.start_datetime,
        "end_datetime": blocked_hours.end_datetime,
    }


@restaurant_router.get("/{restaurant_id}/units/{unit_id}/availability")
def check_availability(
    request: HttpRequest, restaurant_id: str, unit_id: str, check_datetime: datetime
):
    is_available = RestaurantService.is_unit_available(unit_id, check_datetime)
    return {"is_available": is_available}
