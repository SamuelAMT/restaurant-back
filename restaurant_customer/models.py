import uuid
from django.db import models
from django.utils import timezone
from django.db import transaction


class RestaurantCustomer(models.Model):
    restaurant_customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, )
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=70, unique=True)
    country_code = models.CharField(max_length=3, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    restaurants = models.ManyToManyField(
        "restaurant.Restaurant",
        related_name="customer_restaurants",
        null=False,
        blank=False
    )

    units = models.ManyToManyField(
        'unit.Unit',
        related_name='customer_units',
        null=False,
        blank=False
    )

    reservations = models.ManyToManyField(
        "reservation.Reservation",
        related_name="customers"
    )

    class Meta:
        indexes = [
            models.Index(
                fields=["first_name", "last_name", "phone"],
                name="restaurant__name_78fb79_idx",
            )
        ]
        db_table = "restaurant_customer"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def reservations(self):
        return self.customer_reservations.all()

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)

            # Ensure restaurants are set from units if not already done
            if self.units.exists() and not self.restaurants.exists():
                restaurants = set(unit.restaurant for unit in self.units.all() if unit.restaurant)
                if restaurants:
                    self.restaurants.set(restaurants)
                else:
                    raise ValueError("No restaurants found for the associated units")
