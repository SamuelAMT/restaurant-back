from django.db import models
from django.db import IntegrityError
import uuid
from django.utils import timezone
from restaurant_customer.models import RestaurantCustomer
from restaurant.models import Restaurant


class Reservation(models.Model):
    reservation_hash = models.CharField(
        blank=False,
        primary_key=True,
        serialize=False,
        default=uuid.uuid4,
        db_index=True,
    )
    reserver = models.CharField(max_length=100, db_index=True)
    amount_of_people = models.IntegerField()
    amount_of_hours = models.IntegerField()
    start_time = models.TimeField(db_index=True, null=False, blank=False)
    end_time = models.TimeField(db_index=True, null=False, blank=False)
    # TODO: Change to reservation_date in order to avoid conflicts with date field
    date = models.DateField(db_index=True)
    email = models.EmailField(max_length=70, null=False, blank=False)
    country_code = models.CharField(max_length=3, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    observation = models.TextField(max_length=250, null=True, blank=True)
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="reservations",
        null=False,
        blank=False,
    )

    STATUS_CHOICES = [
        ("confirmed", "Confirmed"),
        ("canceled", "Canceled"),
        ("finished", "Finished"),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="confirmed",
    )

    created_at = models.DateTimeField(null=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    customer = models.ForeignKey(
        RestaurantCustomer,
        on_delete=models.CASCADE,
        related_name="customer_reservations",
        null=True,
        blank=True,
    )


    def save(self, *args, **kwargs):
        if not self.pk:
            is_unique = False
            while not is_unique:
                try:
                    super().save(*args, **kwargs)
                    is_unique = True
                except IntegrityError:
                    self.reservation_hash = uuid.uuid4()
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.amount_of_people} - {self.amount_of_hours} - {self.start_time} - {self.end_time} - {self.date} - {self.reservation_hash} - {self.reserver} - {self.email} - {self.country_code} - {self.phone} - {self.birthday} - {self.observation} - {self.restaurant}"

    class Meta:
        indexes = [
            models.Index(
                fields=["reserver", "start_time", "end_time", "date", "reservation_hash"],
                name="reservation_reserve_9df32c_idx",
            )
        ]
