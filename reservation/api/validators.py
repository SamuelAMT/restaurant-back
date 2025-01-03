from django.core.exceptions import ValidationError
from datetime import datetime, time

def validate_reservation_time(start_time: time, end_time: time) -> None:
    """Validate reservation start and end times"""
    if start_time >= end_time:
        raise ValidationError("End time must be after start time")

def validate_reservation_date(reservation_date: datetime) -> None:
    """Validate reservation date is not in the past"""
    if reservation_date.date() < datetime.now().date():
        raise ValidationError("Reservation date cannot be in the past")

def validate_amount_of_people(amount: int) -> None:
    """Validate the number of people for reservation"""
    if amount < 1:
        raise ValidationError("Amount of people must be at least 1")
    if amount > 100:  # Adjust this limit based on the business rules
        raise ValidationError("Amount of people exceeds maximum allowed")