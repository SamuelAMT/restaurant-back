from django import forms
from .models import Reservation
from datetime import datetime, timedelta

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = (
            'reserver',
            'unit',
            'restaurant',
            'reservation_date', 
            'start_time', 
            'end_time',
            'amount_of_people',
            'email', 
            'country_code',
            'phone', 
            'birthday', 
            'observation',
        )

    def clean(self):
        cleaned_data = super().clean()
        unit = cleaned_data.get('unit')
        restaurant = cleaned_data.get('restaurant')
        
        if unit and not restaurant:
            cleaned_data['restaurant'] = unit.restaurant
            
        return cleaned_data