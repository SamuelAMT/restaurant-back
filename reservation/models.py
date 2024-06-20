from django.db import models

# Create your models here.

class Reservation(models.Model):
    amountOfPeople = models.IntegerField()
    amountOfHours = models.IntegerField()
    time = models.IntegerField()
    date = models.DateField()
    hash = models.CharField(max_length=100, primary_key=True)
    reserver = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    