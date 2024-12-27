from ninja import Router
from django.shortcuts import get_object_or_404
from .schemas import ReservationCreateSchema, ReservationResponseSchema
from ..core.services import ReservationService

reservation_router = Router()

@reservation_router.post("/restaurant/{restaurant_id}/reservation", response=ReservationResponseSchema)
def create_reservation(request, restaurant_id: str, payload: ReservationCreateSchema):
    return ReservationService.create_reservation(restaurant_id, payload)