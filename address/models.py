from django.db import models

# Create your models here.

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    cep = models.CharField(max_length=9)
    street = models.CharField(max_length=30)
    number = models.CharField(max_length=10)
    neighborhood = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    country = models.CharField(max_length=30)

    class Meta:
        unique_together = (('cep', 'street', 'street', 'number', 'neighborhood', 'city', 'state', 'country'),)

    def __str__(self):
        return f"{self.id} - {self.cep}, {self.street}, {self.number} - {self.neighborhood}, {self.city} - {self.state} - {self.country}"