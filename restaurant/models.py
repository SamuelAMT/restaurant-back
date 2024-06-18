from django.db import models

# Create your models here.

class Restaurant(models.Model):
    cep = models.CharField(max_length=9)
    street = models.CharField(max_length=30)
    number = models.CharField(max_length=10)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    neighborhood = models.CharField(max_length=30)
    cnpj = models.CharField(max_length=14)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    website = models.URLField()
    description = models.TextField()
    image = models.ImageField(upload_to='restaurant/images')
    def __str__(self):
        return self.name