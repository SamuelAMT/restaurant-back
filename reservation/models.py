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
        editable=False
    )
    reserver = models.CharField(max_length=100)
    amount_of_people = models.PositiveIntegerField()
    amount_of_hours = models.PositiveIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    reservation_date = models.DateField()
    email = models.EmailField(max_length=70)
    country_code = models.CharField(max_length=3, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    observation = models.TextField(max_length=250, blank=True)
    status = models.CharField(
        max_length=20,
        choices=ReservationStatus.choices,
        default=ReservationStatus.CONFIRMED,
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    unit = models.ForeignKey(
        'unit.Unit',
        on_delete=models.CASCADE,
        related_name="reservations",
        null=False
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="reservations",
        null=False
    )
    customer = models.ForeignKey(
        RestaurantCustomer,
        on_delete=models.CASCADE,
        related_name="customer_reservations",
        null=True,
        blank=True
    )

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "reservation_date",
                    "start_time",
                    "end_time",
                ],
                name="reservation_datetime_idx",
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
        if not self.unit or not self.restaurant:
            raise ValidationError("Both unit and restaurant are required")
        if self.unit.restaurant != self.restaurant:
            raise ValidationError("Unit must belong to the specified restaurant")

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to calculate 'amount_of_hours' before saving.
        Ensures 'reservation_hash' is unique by regenerating it in case of IntegrityError.
        """

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
