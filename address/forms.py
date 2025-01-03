from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'cep', 
            'street', 
            'number', 
            'neighborhood', 
            'city', 
            'state', 
            'country', 
            'complement',
            'restaurant',
            'address_id'
        ]
        widgets = {
            'created_at': forms.DateTimeInput(attrs={'readonly': 'readonly'}),
            'updated_at': forms.DateTimeInput(attrs={'readonly': 'readonly'}),
            'address_id': forms.TextInput(attrs={'readonly': 'readonly'})
        }

    def clean_cep(self):
        cep = self.cleaned_data.get('cep')
        # Add CEP validation if needed
        return cep