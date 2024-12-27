from django.db import models
import uuid

class WorkingHours(models.Model):
    WEEKDAYS = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    working_hours_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unit = models.ForeignKey(
        'restaurant.RestaurantUnit',
        on_delete=models.CASCADE,
        related_name='working_hours'
    )
    day_of_week = models.IntegerField(choices=WEEKDAYS)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    is_closed = models.BooleanField(default=False)

    class Meta:
        db_table = 'working_hours'
        unique_together = [['unit', 'day_of_week']]

class BlockedHours(models.Model):
    blocked_hours_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unit = models.ForeignKey(
        'restaurant.RestaurantUnit',
        on_delete=models.CASCADE,
        related_name='blocked_hours'
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'blocked_hours'