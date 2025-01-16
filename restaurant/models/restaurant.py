from django.db import models
from .employee import RestaurantEmployee
from django.conf import settings
from cloudinary.models import CloudinaryField
from custom_auth.models import Role
from restaurant.models.classification import RestaurantCategory, RestaurantCuisineType
import uuid


class Restaurant(models.Model):
    restaurant_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False,
    )
    cnpj = models.CharField(max_length=14, unique=True, db_index=True)
    name = models.CharField(max_length=100, db_index=True)
    country_code = models.CharField(max_length=3)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=70, blank=True, null=True)
    email_verified = models.EmailField(null=True, blank=True)
    image = CloudinaryField("image", null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.RESTAURANT_ADMIN
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="restaurants"
    )
    category = models.ForeignKey(
        RestaurantCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="restaurants",
    )
    cuisine_types = models.ManyToManyField(RestaurantCuisineType, related_name="restaurants")
    customers = models.ManyToManyField(
        "restaurant_customer.RestaurantCustomer",
        related_name="customer_restaurants"
    )
    login_logs = models.ManyToManyField(
        "custom_auth.LoginLog", related_name="restaurants"
    )

    class Meta:
        indexes = [
            models.Index(
                fields=["restaurant_id", "name"], name="restaurant__id_name_idx"
            )
        ]
        db_table = "restaurant"

    def __str__(self):
        return self.name
