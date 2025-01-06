import uuid
from django.db import models
from django.utils import timezone

class RestaurantCustomer(models.Model):
    restaurant_customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    first_name = models.CharField(max_length=30,)
    last_name = models.CharField(max_length=30,)
    email = models.EmailField(max_length=70, unique=True)
    country_code = models.CharField(max_length=3, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(null=False, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    units = models.ManyToManyField(
        'unit.Unit',
        related_name='unit_customers',
        null=True,
        blank=True
    )

    class Meta:
        indexes = [
            models.Index(
                fields=["first_name", "last_name", "phone"], name="restaurant__name_78fb79_idx",
            )
        ]
        db_table = "restaurant_customer"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def reservations(self):
        return self.customer_reservations.all()