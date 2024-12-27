from ninja import Schema
from datetime import date, time
from typing import Optional
from pydantic import EmailStr
from uuid import UUID

class BaseReservationSchema(Schema):
    reserver: str
    amount_of_people: int
    start_time: time
    end_time: time
    reservation_date: date
    email: EmailStr
    country_code: str
    phone: str
    birthday: Optional[date] = None
    observation: Optional[str] = None

class ReservationCreateSchema(BaseReservationSchema):
    pass

class ReservationResponseSchema(BaseReservationSchema):
    reservation_hash: UUID
    status: str