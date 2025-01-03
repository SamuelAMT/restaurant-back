from ninja import Router
from django.http import HttpRequest
from typing import List
from ...services.reservation_service import ReservationService
from ..schemas.reservation import (
    ReservationCreateSchema,
    ReservationResponseSchema,
    ReservationListSchema
)

reservation_router = Router()

@reservation_router.post("/{restaurant_id}/reservations", response=ReservationResponseSchema)
def create_reservation(request: HttpRequest, restaurant_id: str, unit_id: str, payload: ReservationCreateSchema):
    return ReservationService.create_reservation(restaurant_id, unit_id, payload)

@reservation_router.get("/{restaurant_id}/reservations", response=List[ReservationListSchema])
def list_reservations(request: HttpRequest, restaurant_id: str, unit_id: str = None):
    return ReservationService.get_reservations(restaurant_id, unit_id)

@reservation_router.put("/{restaurant_id}/reservations/{reservation_hash}/cancel")
def cancel_reservation(request: HttpRequest, restaurant_id: str, reservation_hash: str):
    return ReservationService.cancel_reservation(restaurant_id, reservation_hash)
