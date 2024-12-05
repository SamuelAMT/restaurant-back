import uuid
from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from ninja import Router, Schema
from typing import Optional
from .models import Reservation
from restaurant.models import Restaurant

reservation_router = Router()

class ReservationRequestSchema(Schema):
# Attach a reservation to a restaurant
    reserver: str
    amount_of_people: int
    amount_of_hours: int
    time: int
    date: str
    email: str
    phone: str
    birthday: Optional[str] = None
    observation: Optional[str] = None

class ReservationResponseSchema(Schema):
    reservation_hash: str
    reserver: str
    amount_of_people: int
    amount_of_hours: int
    time: int
    date: str
    email: str
    phone: str

@reservation_router.post("/restaurant/{restaurant_id}/reservation", response=ReservationResponseSchema)
def create_reservation(request, restaurant_id: str, payload: ReservationRequestSchema):
    restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)

    reservation = Reservation.objects.create(
        restaurant=restaurant,
        reserver=payload.reserver,
        amount_of_people=payload.amount_of_people,
        amount_of_hours=payload.amount_of_hours,
        time=payload.time,
        date=payload.date,
        email=payload.email,
        phone=payload.phone,
        birthday=payload.birthday,
        observation=payload.observation,
        reservation_hash=str(uuid.uuid4()),
    )

    return ReservationResponseSchema(
        reservation_hash=reservation.reservation_hash,
        reserver=reservation.reserver,
        amount_of_people=reservation.amount_of_people,
        amount_of_hours=reservation.amount_of_hours,
        time=reservation.time,
        date=str(reservation.date),
        email=reservation.email,
        phone=reservation.phone,
    )