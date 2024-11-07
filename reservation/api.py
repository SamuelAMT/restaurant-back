from ninja import Router, Schema
from typing import Optional
from restaurant.models import Restaurant
from reservation.models import Reservation
from restaurant.api import ReservationSchema
from django.shortcuts import get_object_or_404

reservation_router = Router()


class CreateReservationSchema(Schema):
    restaurant_id: str
    reserver: str
    amount_of_people: int
    amount_of_hours: int
    time: int
    date: str
    email: str
    phone: str
    birthday: Optional[str] = None


@reservation_router.get("/")
def get_reservations(request):
    return {"reservations": "list of reservations"}


@reservation_router.post("/reservations/", response=ReservationSchema)
def create_reservation(request, payload: CreateReservationSchema):
    restaurant = get_object_or_404(Restaurant, restaurant_id=payload.restaurant_id)
    reservation = Reservation.objects.create(
        reserver=payload.reserver,
        amount_of_people=payload.amount_of_people,
        amount_of_hours=payload.amount_of_hours,
        time=payload.time,
        date=payload.date,
        email=payload.email,
        phone=payload.phone,
        birthday=payload.birthday,
        visit=restaurant,
    )
    return reservation
