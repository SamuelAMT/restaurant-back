from django import forms
from .models import RestaurantCustomer
from restaurant.models import Restaurant

class RestaurantCustomerForm(forms.ModelForm):
    restaurants = forms.ModelMultipleChoiceField(
        queryset=Restaurant.objects.all(),
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
        ]
        widgets = {
            "created_at": forms.DateTimeInput(attrs={"readonly": "readonly"}),
            "updated_at": forms.DateTimeInput(attrs={"readonly": "readonly"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["birthday"].widget = forms.DateInput(attrs={"type": "date"})
        
        if self.instance.pk:
            self.fields['restaurants'].initial = self.instance.restaurants.all()

    def save(self, commit=True):
        instance = super().save(commit=commit)
        if commit and 'restaurants' in self.cleaned_data:
            instance.restaurants.set(self.cleaned_data['restaurants'])
        return instance