from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = (
            'reserver', 
            'reservation_date', 
            'start_time', 
            'end_time',
            'amount_of_people',
            'amount_of_hours',
            'email', 
            'country_code',
            'phone', 
            'birthday', 
            'observation',
            'restaurant',
            'created_at',
            'status'
        )
        widgets = {
            'created_at': forms.DateTimeInput(attrs={'readonly': 'readonly'}),
            'status': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'amount_of_hours' in self.fields:
            self.fields['amount_of_hours'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time:
            # Calculate amount of hours
            time_difference = end_time - start_time
            hours_difference = time_difference.total_seconds() / 3600
            cleaned_data['amount_of_hours'] = round(hours_difference, 2)
            
        return cleaned_data