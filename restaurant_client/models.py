from django.db import models

class RestaurantClient(models.Model):
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    country_code = models.CharField(max_length=3)
    phone = models.CharField(max_length=20, primary_key=True)
    email = models.EmailField(max_length=70, blank=True, null=True,)
    birthdate = models.DateField(blank=True, null=True,)
    
    # Adapted to avoid circular imports error
    # Instead it's calling the model as a string to avoid it
    reservations = models.ManyToManyField(
        'reservation.Reservation',
        related_name='restaurant_clients'       
    )
    
    def __str__(self):
        return self.name