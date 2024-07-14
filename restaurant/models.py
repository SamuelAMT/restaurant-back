from django.db import models
from restaurant_customer.models import RestaurantCustomer

class Restaurant(models.Model):
    cnpj = models.CharField(max_length=14, primary_key=True, db_index=True, db_tablespace='index_tablespace')
    name = models.CharField(max_length=100, db_index=True)
    country_code = models.CharField(max_length=3, blank=True, null=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=70, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    
    customers = models.ManyToManyField(
        'restaurant_customer.RestaurantCustomer',
        related_name='restaurants'
    )
    
    class Meta:
        db_tablespace = 'tables'
        indexes = [models.Index(fields=['cnpj', 'name'], db_tablespace='other_index_tablespace')]

    def __str__(self):
        return self.name