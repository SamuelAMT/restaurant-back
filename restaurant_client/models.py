from django.db import models

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    country_code = models.CharField(max_length=3)
    phone = models.CharField(max_length=20, primary_key=True)
    """ email = models.EmailField() """
    """ birthdate = models.DateField(blank=True, null=False) """
    def __str__(self):
        return self.name