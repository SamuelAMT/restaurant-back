from django import forms
from django.core.exceptions import ValidationError
from .models import RestaurantCustomer
from unit.models.unit import Unit

class RestaurantCustomerForm(forms.ModelForm):
    units = forms.ModelMultipleChoiceField(
        queryset=Unit.objects.all(),
        required=True,
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['units'].initial = self.instance.units.all()

    def clean(self):
        cleaned_data = super().clean()
        units = cleaned_data.get('units')

        if not units:
            raise ValidationError("At least one unit must be selected.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            if self.cleaned_data.get('units'):
                instance.units.set(self.cleaned_data['units'])
                # Set restaurants based on the selected units
                unit_restaurants = {unit.restaurant for unit in self.cleaned_data['units']}
                instance.restaurants.set(unit_restaurants)
        return instance