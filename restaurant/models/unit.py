from django.db import models
import uuid

class RestaurantUnit(models.Model):
    unit_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.ForeignKey(
        'restaurant.Restaurant',
        on_delete=models.CASCADE,
        related_name='units'
    )
    name = models.CharField(max_length=100)
    is_main_unit = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'restaurant_unit'
        unique_together = [['restaurant', 'name']]

    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"