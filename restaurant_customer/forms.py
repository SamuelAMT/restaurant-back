from django import forms
from .models import RestaurantCustomer
from restaurant.models import Restaurant
from unit.models.unit import Unit

class RestaurantCustomerForm(forms.ModelForm):
    restaurants = forms.ModelMultipleChoiceField(
        queryset=Restaurant.objects.all(),
        required=False,
        widget=forms.SelectMultiple(),
    )
    units = forms.ModelMultipleChoiceField(
        queryset=Unit.objects.all(),
        required=False,
        widget=forms.SelectMultiple(),
    )

    class Meta:
        model = RestaurantCustomer
        fields = [
            "first_name",
            "last_name",
            "email",
            "country_code",
            "phone",
            "birthday",
            "restaurants",
            "units",
        ]
        widgets = {
            "created_at": forms.DateTimeInput(attrs={"readonly": "readonly"}),
            "updated_at": forms.DateTimeInput(attrs={"readonly": "readonly"}),
            "birthday": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['restaurants'].initial = self.instance.restaurants.all()
            self.fields['units'].initial = self.instance.units.all()

    def clean(self):
        cleaned_data = super().clean()
        unit = cleaned_data.get('units')
        restaurants = cleaned_data.get('restaurants')

        # Add restaurants of selected units if not already selected
        if unit:
            unit_restaurants = set(unit.restaurant for unit in unit)
            if restaurants:
                restaurants = set(restaurants)
                restaurants.update(unit_restaurants)
            else:
                restaurants = unit_restaurants
            cleaned_data['restaurants'] = list(restaurants)

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=commit)
        if commit and 'restaurants' in self.cleaned_data:
            instance.restaurants.set(self.cleaned_data['restaurants'])
        return instance