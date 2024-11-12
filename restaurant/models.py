from django.db import models
from custom_auth.models import Role
import uuid

class Restaurant(models.Model):
    restaurant_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, db_index=True)
    cnpj = models.CharField(max_length=14, unique=True, db_index=True)
    name = models.CharField(max_length=100, db_index=True)
    country_code = models.CharField(max_length=3, blank=False, null=False)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=70, blank=True, null=True)
    email_verified = models.EmailField(null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.RESTAURANT_ADMIN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    customers = models.ManyToManyField("restaurant_customer.RestaurantCustomer", related_name="restaurants")
    #accounts = models.ManyToManyField('custom_auth.Account', related_name='restaurants')
    addresses = models.ManyToManyField('address.Address', related_name='restaurants')
    employees = models.ManyToManyField('RestaurantEmployee', related_name='restaurants')
    login_logs = models.ManyToManyField('custom_auth.LoginLog', related_name='restaurants')

    class Meta:
        indexes = [
            models.Index(fields=['restaurant_id', 'name'], name='restaurant__id_name_idx'),
        ]

    def __str__(self):
        return self.name


class RestaurantEmployee(models.Model):
    restaurant_employee_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, db_index=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=70, unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.RESTAURANT_STAFF)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='staff')

    def __str__(self):
        return self.name or self.email
