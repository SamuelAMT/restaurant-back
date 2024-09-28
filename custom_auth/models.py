from django.db import models
from restaurant.models import Restaurant, RestaurantEmployee

class Role(models.TextChoices):
    RESTAURANTCUSTOMER = 'RESTAURANTCUSTOMER', 'RestaurantCustomer'
    ADMIN = 'ADMIN', 'Admin'
    RESTAURANT = 'RESTAURANT', 'Restaurant'
    RESTAURANTEMPLOYEE = 'RESTAURANTEMPLOYEE', 'RestaurantEmployee'
    
class Account(models.Model):
    type = models.CharField(max_length=50)
    provider = models.CharField(max_length=50)
    provider_account_id = models.CharField(max_length=100)
    refresh_token = models.CharField(max_length=200, null=True, blank=True)
    access_token = models.CharField(max_length=200, null=True, blank=True)
    expires_at = models.IntegerField(null=True, blank=True)
    token_type = models.CharField(max_length=50, null=True, blank=True)
    scope = models.CharField(max_length=100, null=True, blank=True)
    id_token = models.CharField(max_length=500, null=True, blank=True)
    session_state = models.CharField(max_length=100, null=True, blank=True)
    
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='accounts', null=True, blank=True)
    employee = models.ForeignKey(RestaurantEmployee, on_delete=models.CASCADE, related_name='accounts', null=True, blank=True)

    def __str__(self):
        return f"Account {self.provider} - {self.provider_account_id}"

class Session(models.Model):
    session_token = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='sessions')
    expires = models.DateTimeField()

    def __str__(self):
        return f"Session {self.session_token}"

class VerificationToken(models.Model):
    identifier = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    expires = models.DateTimeField()

    def __str__(self):
        return f"Token for {self.identifier}"
