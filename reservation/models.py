from django.db import models
from django.db import IntegrityError
import uuid
from django.utils import timezone
from datetime import timedelta, datetime
from django.core.exceptions import ValidationError
from restaurant_customer.models import RestaurantCustomer
from restaurant.models import Restaurant
from .core.constants import ReservationStatus


class Reservation(models.Model):
    reservation_hash = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    reserver = models.CharField(max_length=100, db_index=True)
    amount_of_people = models.PositiveIntegerField()
    amount_of_hours = models.PositiveIntegerField(editable=False)
    start_time = models.TimeField(db_index=True)
    end_time = models.TimeField(db_index=True)
    reservation_date = models.DateField(db_index=True)
    email = models.EmailField(max_length=70)
    country_code = models.CharField(max_length=3, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    observation = models.TextField(max_length=250, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=ReservationStatus.choices,
        default=ReservationStatus.CONFIRMED,
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="reservations",
    )
    customer = models.ForeignKey(
        RestaurantCustomer,
        on_delete=models.CASCADE,
        related_name="customer_reservations",
        null=True,
        blank=True,
    )

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "reserver",
                    "start_time",
                    "end_time",
                    "reservation_date",
                    "reservation_hash",
                ],
                name="reservation_idx",
            )
        ]
        db_table = "reservation"
        constraints = [
            models.CheckConstraint(
                check=models.Q(amount_of_people__gt=0),
                name='positive_people_amount'
            ),
        ]

    def __str__(self):
        return f"Reservation {self.reservation_hash} - {self.reserver} ({self.reservation_date})"

    def clean(self):
        super().clean()
        errors = {}

        # Add validation for restaurant working hours (to be implemented when Restaurant model is updated)
        if hasattr(self.restaurant, 'working_hours'):
            # Placeholder for the upcoming Restaurant blocking hours journey feature
            pass

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to calculate 'amount_of_hours' before saving.
        Ensures 'reservation_hash' is unique by regenerating it in case of IntegrityError.
        """
        if self.start_time and self.end_time:
            start_datetime = datetime.combine(self.reservation_date, self.start_time)
            end_datetime = datetime.combine(self.reservation_date, self.end_time)
            
            # If end_time is less than start_time, assume the reservation ends the next day
            if end_datetime < start_datetime:
                end_datetime += timedelta(days=1)
            
            # Calculate the difference in hours and round up to the nearest hour
            time_difference = end_datetime - start_datetime
            hours = time_difference.total_seconds() / 3600
            self.amount_of_hours = int(hours) if hours.is_integer() else int(hours) + 1

        self.full_clean()

        if not self.pk:  # Only for new reservations
            is_unique = False
            while not is_unique:
                try:
                    super().save(*args, **kwargs)
                    is_unique = True
                except IntegrityError:
                    self.reservation_hash = uuid.uuid4()
        else:
            super().save(*args, **kwargs)