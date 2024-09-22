#from django.db import models
#from django.db import IntegrityError
#import uuid
#class RestaurantVisit(models.Model):
#   restaurant = models.ForeignKey(
#       "restaurant.Restaurant",
#       on_delete=models.CASCADE,
#       related_name="restaurant_visits",
#   )
#   """ restaurant_customer = models.ForeignKey(
#       'restaurant_customer.RestaurantCustomer',
#       on_delete=models.CASCADE,
#       related_name='restaurant_visits',
#   ) """
#class Reservation(models.Model):
#   reserver = models.CharField(max_length=100, db_index=True)
#   amount_of_people = models.IntegerField()
#   amount_of_hours = models.IntegerField()
#   time = models.IntegerField(db_index=True)
#   date = models.DateField(db_index=True)
#   reservation_hash = models.CharField(
#       max_length=100,
#       unique=True,
#       blank=False,
#       primary_key=True,
#       serialize=False,
#       default=uuid.uuid4,
#       db_index=True,
#   )
#   class Meta:
#       indexes = [
#           models.Index(
#               fields=["reserver", "time", "date", "reservation_hash"],
#               name="reservation_reserve_9df32c_idx",
#           )
#       ]
#   visit = models.ForeignKey(
#       RestaurantVisit,
#       on_delete=models.CASCADE,
#       related_name="reservations",
#   )
#   def save(self, *args, **kwargs):
#       if not self.pk:
#           is_unique = False
#           while not is_unique:
#               try:
#                   super().save(*args, **kwargs)
#                   is_unique = True
#               except IntegrityError:
#                   self.reservation_hash = uuid.uuid4()
#       else:
#           super().save(*args, **kwargs)
#   def __str__(self):
#       return f"{self.amount_of_people} - {self.amount_of_hours} - {self.time} - {self.date} - {self.reservation_hash} - {self.reserver}"
#