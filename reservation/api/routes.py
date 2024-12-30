from ninja import Router
from uuid import UUID
from typing import Optional
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from .schemas import (
    ReservationCreateSchema,
    ReservationResponseSchema,
)
from ..core.services import ReservationService

reservation_router = Router()

@reservation_router.post(
    "/restaurant/{restaurant_id}",
    response=ReservationResponseSchema
)
def create_reservation(
    request: HttpRequest,
    restaurant_id: str,
    payload: ReservationCreateSchema
):
    return ReservationService.create_reservation(restaurant_id, payload)

@reservation_router.get(
    "/restaurant/{restaurant_id}",
    response=list[ReservationResponseSchema]
)
def list_reservations(
    request: HttpRequest,
    restaurant_id: str,
    unit_id: Optional[UUID] = None,
):
    return ReservationService.get_reservations(
        restaurant_id=restaurant_id,
        unit_id=unit_id,
    )
