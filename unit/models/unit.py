from django.db import models
import uuid
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from reservation.models import ReservationStatus
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

    def clean(self):
        super().clean()
        # Ensure working hours are set for all days
        days_with_hours = set(
            self.working_hours.values_list('day_of_week', flat=True)
        )
        missing_days = set(range(7)) - days_with_hours
        if missing_days and not self._state.adding:
            raise ValidationError(
                f"Working hours not set for days: {', '.join(str(d) for d in missing_days)}"
            )

    def is_available_for_reservation(self, start_datetime, end_datetime):
        """
        Check if unit is available for reservation at given time range
        """
        # Check working hours
        working_hours = self.working_hours.filter(
            day_of_week=start_datetime.weekday()
        ).first()

        if not working_hours or working_hours.is_closed:
            return False, "Unit is closed on this day"

        if (start_datetime.time() < working_hours.opening_time or
                end_datetime.time() > working_hours.closing_time):
            return False, "Time is outside working hours"

        # Check blocked hours
        blocked = self.blocked_hours.filter(
            start_datetime__lte=end_datetime,
            end_datetime__gte=start_datetime
        ).exists()

        if blocked:
            return False, "Time slot is blocked"

        # Check existing reservations
        conflicting = self.reservations.filter(
            reservation_date=start_datetime.date(),
            status=ReservationStatus.CONFIRMED,
            start_time__lt=end_datetime.time(),
            end_time__gt=start_datetime.time()
        ).exists()

        if conflicting:
            return False, "Time slot is already reserved"

        return True, "Available"

    def get_availability_calendar(self, start_date, end_date):
        """
        Returns calendar with available slots for the date range
        """
        calendar = {}
        delta = end_date - start_date

        for i in range(delta.days + 1):
            current_date = start_date + timedelta(days=i)
            working_hours = self.working_hours.filter(
                day_of_week=current_date.weekday()
            ).first()

            if not working_hours or working_hours.is_closed:
                calendar[current_date] = []
                continue

            # Get blocked hours
            blocked_times = self.blocked_hours.filter(
                start_datetime__date=current_date
            ).values_list('start_datetime', 'end_datetime')

            # Get existing reservations
            reservations = self.reservations.filter(
                reservation_date=current_date,
                status=ReservationStatus.CONFIRMED
            ).values_list('start_time', 'end_time')

            # Calculate available slots
            available_slots = []
            current_time = working_hours.opening_time

            while current_time < working_hours.closing_time:
                slot_end = (
                        datetime.combine(current_date, current_time) +
                        timedelta(hours=1)
                ).time()

                is_available = True

                # Check if slot conflicts with blocked hours
                for block_start, block_end in blocked_times:
                    if (current_time < block_end.time() and
                            slot_end > block_start.time()):
                        is_available = False
                        break

                # Check if slot conflicts with reservations
                for res_start, res_end in reservations:
                    if current_time < res_end and slot_end > res_start:
                        is_available = False
                        break

                if is_available:
                    available_slots.append({
                        'start': current_time,
                        'end': slot_end
                    })

                current_time = slot_end

            calendar[current_date] = available_slots

        return calendar

    def save(self, *args, **kwargs):
        if self.is_main_unit:
            Unit.objects.filter(
                restaurant=self.restaurant,
                is_main_unit=True
            ).exclude(unit_id=self.unit_id).update(is_main_unit=False)
        super().save(*args, **kwargs)