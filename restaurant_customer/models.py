import uuid
from django.db import models

class RestaurantCustomer(models.Model):
    restaurant_customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=70, unique=True)
    country_code = models.CharField(max_length=3, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        indexes = [
            models.Index(
                fields=["name", "lastname", "phone"], name="restaurant__name_78fb79_idx"
            )
        ]

    def __str__(self):
        return f"{self.name} {self.lastname}"
    
    @property
    def reservations(self):
        return self.customer_reservations.all()