from django.db import models

class RestaurantClient(models.Model):
    name = models.CharField(max_length=100, db_index=True, db_tablespace='index_tablespace')
    lastname = models.CharField(max_length=100, db_index=True, db_tablespace='index_tablespace')
    country_code = models.CharField(max_length=3)
    phone = models.CharField(max_length=20, primary_key=True, db_index=True, db_tablespace='index_tablespace')
    email = models.EmailField(max_length=70, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True,)
    
    # Adapted to avoid circular imports error
    # Instead it's calling the model as a string to avoid it
    reservations = models.ManyToManyField(
        'reservation.Reservation',
        related_name='restaurant_clients'
    )
    
    class Meta:
        db_tablespace = 'tables'
        indexes = [models.Index(fields=['name', 'lastname', 'phone'], db_tablespace='other_index_tablespace')]
    
    def __str__(self):
        return self.name