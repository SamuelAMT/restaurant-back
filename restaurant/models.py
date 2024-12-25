from django.db import models
from custom_auth.models import Role
import uuid
from django.conf import settings
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError

class Restaurant(models.Model):
    restaurant_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    cnpj = models.CharField(max_length=14, unique=True, db_index=True)
    name = models.CharField(max_length=100, db_index=True)
    country_code = models.CharField(max_length=3, blank=False, null=False)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=70, blank=True, null=True)
    email_verified = models.EmailField(null=True, blank=True)
    image = CloudinaryField('image', null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.RESTAURANT_ADMIN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='restaurants')

    customers = models.ManyToManyField("restaurant_customer.RestaurantCustomer", related_name="restaurants")
    #accounts = models.ManyToManyField('custom_auth.Account', related_name='restaurants')
    #addresses = models.OneToOneField('address.Address',on_delete=models.CASCADE, related_name='restaurants')
    employees = models.ManyToManyField('RestaurantEmployee', related_name='restaurants')
    login_logs = models.ManyToManyField('custom_auth.LoginLog', related_name='restaurants')

    class Meta:
        indexes = [models.Index(fields=['restaurant_id', 'name'], name='restaurant__id_name_idx')]
        db_table = 'restaurant'

    def __str__(self):
        return self.name


class RestaurantEmployee(models.Model):
    restaurant_employee_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, db_index=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=70, unique=True)
    country_code = models.CharField(max_length=3, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.RESTAURANT_STAFF)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='staff')

    class Meta:
        indexes = [
            models.Index(
                fields=["first_name", "last_name", "phone"], name="restaurant__employee_idx"
            )
        ]
        db_table = 'restaurant_employee'

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"
