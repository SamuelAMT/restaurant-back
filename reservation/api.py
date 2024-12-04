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
    restaurant_id: str
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

@reservation_router.post("/reservation", response=ReservationResponseSchema)
def create_reservation(request: HttpRequest, payload: ReservationRequestSchema):
    restaurant = get_restaurant_from_request(request)

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
        date=reservation.date,
        email=reservation.email,
        phone=reservation.phone,
    )