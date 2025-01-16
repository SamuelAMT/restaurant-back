from django import forms
from .models import Address
from unit.models.unit import Unit

class AddressForm(forms.ModelForm):
    unit = forms.ModelChoiceField(
        queryset=Unit.objects.all(),
        required=True,
        label='Unit'
    )

    class Meta:
        model = Address
        fields = [
            "cep",
            "street",
            "number",
            "neighborhood",
            "city",
            "state",
            "country",
            "complement",
            "maps_url",
        ]
        widgets = {
            "complement": forms.TextInput(attrs={"placeholder": "Apartment, suite, etc."}),
        }

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        address = super().save(commit=commit)
        if commit:
            unit = self.cleaned_data['unit']
            unit.address = address
            unit.save()
        return address

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = ['cep', 'street', 'number', 'neighborhood', 'city', 'state', 'country']
        for field in required_fields:
            self.fields[field].required = True
        
        if self.instance and hasattr(self.instance, 'unit'):
            self.fields['unit'].initial = self.instance.unit