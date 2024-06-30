from django.db import models
from restaurant.models import Restaurant

# Change the class name to Place
class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    cep = models.CharField(max_length=9)
    street = models.CharField(max_length=30)
    number = models.CharField(max_length=10)
    neighborhood = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    country = models.CharField(max_length=30)
    
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='addresses',
        null=True,
    )

    class Meta:
        unique_together = (('cep', 'street', 'number', 'neighborhood', 'city', 'state', 'country'),)

    def __str__(self):
        return f"{self.address_id} - {self.cep}, {self.street}, {self.number} - {self.neighborhood}, {self.city} - {self.state} - {self.country}"