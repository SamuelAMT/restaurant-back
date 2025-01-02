from django import forms
from .models import Address


class AddressForm(forms.ModelForm):
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
            "unit",
            "address_id",
        ]
        widgets = {
            "created_at": forms.DateTimeInput(attrs={"readonly": "readonly"}),
            "updated_at": forms.DateTimeInput(attrs={"readonly": "readonly"}),
            "address_id": forms.TextInput(attrs={"readonly": "readonly"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
