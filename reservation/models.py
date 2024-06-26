from django.db import models
from django.db import IntegrityError
import uuid

class Reservation(models.Model):
    amount_of_people = models.IntegerField()
    amount_of_hours = models.IntegerField()
    time = models.IntegerField()
    date = models.DateField()
    reservation_hash = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        primary_key=True,
        default=uuid.uuid4,
    )
    
    reserver = models.CharField(max_length=100)
    
    # Adapted to avoid circular imports error
    # Instead it's calling the model as a string to avoid it
    restaurant_client = models.ForeignKey(
        'restaurant_client.RestaurantClient',
        on_delete=models.CASCADE,
        related_name='client_reservations',
        null=True,   
    )
    
    # Adapted to avoid circular imports error
    # Instead it's calling the model as a string to avoid it
    restaurant = models.ForeignKey(
        'restaurant.Restaurant',
        on_delete=models.CASCADE,
        null=True,  
    )
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the instance is not already saved
            is_unique = False
            while not is_unique:
                try:
                    super().save(*args, **kwargs)
                    is_unique = True
                except IntegrityError:
                    self.reservation_hash = uuid.uuid4()  # Generate a new UUID if there was a collision
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.amount_of_people} - {self.amount_of_hours} - {self.time} - {self.date} - {self.hash} - {self.reserver}"