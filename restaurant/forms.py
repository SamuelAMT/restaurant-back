from django import forms
from .models import Restaurant, RestaurantEmployee

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ('name', 'cnpj', 'country_code', 'phone', 'email', 'website',
                 'description', 'image', 'role', 'admin')

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class RestaurantEmployeeForm(forms.ModelForm):
    class Meta:
        model = RestaurantEmployee
        fields = ['first_name', 'last_name', 'email', 'country_code', 'phone', 'role', 'restaurant']
