from ninja import Router
from django.http import HttpRequest
from typing import List
from reservation.services import ReservationService
from ..schemas.reservation import (
    ReservationCreateSchema,
    ReservationResponseSchema,
    ReservationListSchema
)

unit_reservation_router = Router()

@unit_reservation_router.post("/{restaurant_id}/units/{unit_id}/reservations", response=ReservationResponseSchema)
def create_reservation(request: HttpRequest, restaurant_id: str, unit_id: str, payload: ReservationCreateSchema):
    return ReservationService.create_reservation(restaurant_id, unit_id, payload)

@unit_reservation_router.get("/{restaurant_id}/units/{unit_id}/reservations", response=List[ReservationListSchema])
def list_unit_reservations(request: HttpRequest, restaurant_id: str, unit_id: str):
    return ReservationService.get_reservations(restaurant_id, unit_id)

@unit_reservation_router.put("/{restaurant_id}/units/{unit_id}/reservations/{reservation_hash}/cancel")
def cancel_reservation(request: HttpRequest, restaurant_id: str, unit_id: str, reservation_hash: str):
    return ReservationService.cancel_reservation(restaurant_id, reservation_hash)