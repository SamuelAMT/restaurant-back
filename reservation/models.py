from django.db import models

# Create your models here.

class Reservation(models.Model):
    amountOfPeople = models.IntegerField(max_length=2)
    amountOfHours = models.IntegerField(max_length=5)
    time = models.IntegerField(max_length=5)
    date = models.DateField()
    hash = models.CharField(max_length=100)
    reserver = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    