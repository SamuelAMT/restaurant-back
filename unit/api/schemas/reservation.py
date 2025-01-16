from ninja import Schema, ModelSchema
from datetime import date, time
from typing import List, Optional
from pydantic import EmailStr
from ...models import Reservation

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

class ReservationResponseSchema(ModelSchema):
    class Config:
        model = Reservation
        model_fields = ['reservation_hash', 'reserver', 'amount_of_people', 
                       'amount_of_hours', 'start_time', 'end_time', 
                       'reservation_date', 'email', 'country_code', 'phone', 
                       'birthday', 'observation', 'status']
