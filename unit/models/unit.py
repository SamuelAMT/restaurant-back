from django.db import models
import uuid
from restaurant.models import Restaurant


class Unit(models.Model):
    unit_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    is_main_unit = models.BooleanField(default=False)
    restaurant = models.ForeignKey(
        'restaurant.Restaurant',
        on_delete=models.CASCADE,
        related_name='units',
        null=False,
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'restaurant_unit'
        unique_together = [['restaurant', 'name']]

    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"

    def save(self, *args, **kwargs):
        if self.is_main_unit:
            Unit.objects.filter(
                restaurant=self.restaurant,
                is_main_unit=True
            ).exclude(unit_id=self.unit_id).update(is_main_unit=False)
        super().save(*args, **kwargs)
