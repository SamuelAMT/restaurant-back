from django.db import models
from restaurant_client.models import RestaurantClient

class Restaurant(models.Model):
    cnpj = models.CharField(max_length=14, primary_key=True)
    name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=3)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=70, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    
    clients = models.ManyToManyField(
        RestaurantClient,
        related_name='restaurants'
    )

    def __str__(self):
        return self.name