from django.db import models

class ReservationStatus(models.TextChoices):
    CONFIRMED = "confirmed", "Confirmed"
    CANCELED = "canceled", "Canceled"
    FINISHED = "finished", "Finished"