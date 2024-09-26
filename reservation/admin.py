from ninja import Router, Schema
from django.http import HttpRequest
from reservation.models import Reservation, RestaurantVisit
from restaurant_customer.models import RestaurantCustomer
from django.shortcuts import get_object_or_404
import uuid

router = Router()


class ReservationRequestSchema(Schema):
    reserver: str
    amount_of_people: int
    amount_of_hours: int
    time: int
    date: str
    email: str
    phone: str
    # visit_id: int


class ReservationResponseSchema(Schema):
    reservation_hash: str
    reserver: str
    amount_of_people: int
    amount_of_hours: int
    time: int
    date: str
    email: str
    phone: str


@router.post("/customer-reservation", response=ReservationResponseSchema)
def create_reservation(request: HttpRequest, payload: ReservationRequestSchema):
    visit = get_object_or_404(RestaurantVisit, id=payload.visit_id)

    reservation = Reservation(
        reserver=payload.reserver,
        amount_of_people=payload.amount_of_people,
        amount_of_hours=payload.amount_of_hours,
        time=payload.time,
        date=payload.date,
        reservation_hash=str(uuid.uuid4()),
        visit=visit,
    )

    reservation.save()

    return ReservationResponseSchema(
        reservation_hash=reservation.reservation_hash,
        reserver=reservation.reserver,
        amount_of_people=reservation.amount_of_people,
        amount_of_hours=reservation.amount_of_hours,
        time=reservation.time,
        date=reservation.date,
        email=payload.email,
        phone=payload.phone,
    )
