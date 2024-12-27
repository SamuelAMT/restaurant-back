from django import forms
from .models import Reservation
from datetime import datetime, timedelta

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = (
            'reserver', 
            'reservation_date', 
            'start_time', 
            'end_time',
            'amount_of_people',
            'email', 
            'country_code',
            'phone', 
            'birthday', 
            'observation',
            'restaurant',
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Calculate amount_of_hours before saving
        if self.cleaned_data.get('start_time') and self.cleaned_data.get('end_time'):
            start_datetime = datetime.combine(datetime.today(), self.cleaned_data['start_time'])
            end_datetime = datetime.combine(datetime.today(), self.cleaned_data['end_time'])
            
            # If end_time is less than start_time, assume it's for the next day
            if end_datetime < start_datetime:
                end_datetime += timedelta(days=1)
            
            # Calculate hours difference and round up to nearest hour
            time_difference = end_datetime - start_datetime
            hours = time_difference.total_seconds() / 3600
            instance.amount_of_hours = int(hours) if hours.is_integer() else int(hours) + 1

        if commit:
            instance.save()
        return instance