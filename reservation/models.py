from django.db import models
from django.db import IntegrityError
import uuid
from django.utils import timezone
from restaurant_customer.models import RestaurantCustomer


class RestaurantVisit(models.Model):
    restaurant = models.ForeignKey(
        "restaurant.Restaurant",
        on_delete=models.CASCADE,
        related_name="visits",
    )
    customer = models.ForeignKey(
        "restaurant_customer.RestaurantCustomer",
        on_delete=models.CASCADE,
        related_name="visits",
        null=True,
    )


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
    time = models.IntegerField(db_index=True)
    date = models.DateField(db_index=True)
    birthday = models.DateField(null=True, blank=True)
    observation = models.TextField(max_length=250, null=True, blank=True)
    
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("canceled", "Canceled"),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
        )
    
    created_at = models.DateTimeField(null=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    customer = models.ForeignKey(
        RestaurantCustomer,
        on_delete=models.CASCADE,
        related_name="customer_reservations",
        null=True
    )

    visit = models.ForeignKey(
        RestaurantVisit,
        on_delete=models.CASCADE,
        related_name="reservations",
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
        return f"{self.amount_of_people} - {self.amount_of_hours} - {self.time} - {self.date} - {self.reservation_hash} - {self.reserver}"

    class Meta:
        indexes = [
            models.Index(
                fields=["reserver", "time", "date", "reservation_hash"],
                name="reservation_reserve_9df32c_idx",
            )
        ]
