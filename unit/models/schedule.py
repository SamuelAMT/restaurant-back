from django.db import models
import uuid
from .unit import Unit
from django.core.exceptions import ValidationError

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
        'unit.Unit',
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

    def clean(self):
        super().clean()
        if self.opening_time >= self.closing_time:
            raise ValidationError("Opening time must be before closing time")

    def is_available(self, datetime_obj):
        """Check if the unit is available at given datetime"""
        if self.is_closed:
            return False

        time = datetime_obj.time()
        return self.opening_time <= time <= self.closing_time

class BlockedHours(models.Model):
    blocked_hours_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unit = models.ForeignKey(
        'unit.Unit',
        on_delete=models.CASCADE,
        related_name='blocked_hours'
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'blocked_hours'
        ordering = ['-start_datetime']
        
    def __str__(self):
        return f"{self.unit.name} - Blocked: {self.start_datetime.strftime('%Y-%m-%d %H:%M')} to {self.end_datetime.strftime('%Y-%m-%d %H:%M')}"

    def clean(self):
        super().clean()
        if self.start_datetime >= self.end_datetime:
            raise ValidationError("Start time must be before end time")

        working_hours = self.unit.working_hours.filter(
            day_of_week=self.start_datetime.weekday()
        ).first()

        if not working_hours:
            raise ValidationError("No working hours defined for this day")

        if (self.start_datetime.time() < working_hours.opening_time or
              self.end_datetime.time() > working_hours.closing_time):
            raise ValidationError("Blocked hours must fall within working hours")

