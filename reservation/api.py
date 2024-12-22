import uuid
from datetime import datetime, date, time
from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from ninja import Router, Schema
from typing import Optional
from pydantic import EmailStr
from .models import Reservation
from restaurant.models import Restaurant
from restaurant_customer.models import RestaurantCustomer

reservation_router = Router()

class ReservationResponseSchema(Schema):
    reservation_hash: str
    reserver: str
    amount_of_people: int
    amount_of_hours: int
    start_time: time
    end_time: time
    reservation_date: date
    email: EmailStr
    country_code: str
    phone: str
    birthday: Optional[date] = None
    observation: Optional[str] = None

class ReservationCreateSchema(Schema):
    reserver: str
    amount_of_people: int
    amount_of_hours: int
    start_time: time
    end_time: time
    reservation_date: date
    email: EmailStr
    country_code: str
    phone: str
    birthday: Optional[date] = None
    observation: Optional[str] = None


@reservation_router.post("/restaurant/{restaurant_id}/reservation", response=ReservationResponseSchema)
def create_reservation(request, restaurant_id: str, payload: ReservationCreateSchema):
    restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
    
    customer, created = RestaurantCustomer.objects.get_or_create(
        email=payload.email,
        defaults={
            'name': payload.reserver,
            'lastname': '',
            'country_code': payload.country_code,
            'phone': payload.phone,
            'birthday': payload.birthday,
        }
    )

    reservation = Reservation.objects.create(
        restaurant=restaurant,
        reserver=payload.reserver,
        amount_of_people=payload.amount_of_people,
        amount_of_hours=payload.amount_of_hours,
        start_time=payload.start_time,
        end_time=payload.end_time,
        reservation_date=payload.reservation_date,
        email=payload.email,
        country_code=payload.country_code,
        phone=payload.phone,
        birthday=payload.birthday,
        observation=payload.observation,
    )

    return ReservationCreateSchema(
        reservation_hash=reservation.reservation_hash,
        reserver=reservation.reserver,
        amount_of_people=reservation.amount_of_people,
        amount_of_hours=reservation.amount_of_hours,
        start_time=reservation.start_time,
        end_time=payload.end_time,
        reservation_date=(reservation.reservation_date),
        email=reservation.email,
        country_code=reservation.country_code,
        phone=reservation.phone,
        birthday=reservation.birthday,
        observation=reservation.observation,
    )