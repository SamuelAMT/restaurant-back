from django.db import models

# Create your models here.

class Reservation(models.Model):
    amount_of_people = models.IntegerField()
    amount_of_hours = models.IntegerField()
    time = models.IntegerField()
    date = models.DateField()
    hash = models.CharField(max_length=100, primary_key=True)
    reserver = models.CharField(max_length=100)
