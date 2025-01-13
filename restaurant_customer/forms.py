from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import RestaurantCustomer
from unit.models.unit import Unit

class RestaurantCustomerForm(forms.ModelForm):
    units = forms.ModelMultipleChoiceField(
        queryset=Unit.objects.all(),
        required=True,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
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
            self.fields['units'].initial = self.instance.units.all()

    def clean_units(self):
        units = self.cleaned_data.get('units')
        if not units:
            raise ValidationError("At least one unit must be selected.")

        # Verify each unit has a restaurant
        for unit in units:
            if not hasattr(unit, 'restaurant') or not unit.restaurant:
                raise ValidationError(f"Unit '{unit}' has no associated restaurant.")

        return units

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            with transaction.atomic():
                # Save the instance first
                instance.save()

                # Set the units
                if self.cleaned_data.get('units'):
                    instance.units.set(self.cleaned_data['units'])

                    # Get unique restaurants from units
                    restaurants = []
                    for unit in self.cleaned_data['units']:
                        if unit.restaurant and unit.restaurant not in restaurants:
                            restaurants.append(unit.restaurant)

                    # Ensure we have restaurants before setting
                    if not restaurants:
                        raise ValidationError("No restaurants found for the selected units")

                    # Set the restaurants explicitly
                    instance.restaurants.set(restaurants)

        return instance
