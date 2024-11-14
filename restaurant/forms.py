# restaurant/forms.py
from django import forms
from .models import Restaurant
from custom_auth.models import CustomUser

class RestaurantAdminForm(forms.ModelForm):
    admin_email = forms.EmailField(label='Admin Email', required=False)
    admin_first_name = forms.CharField(label='Admin First Name', required=False)
    admin_last_name = forms.CharField(label='Admin Last Name', required=False)

    class Meta:
        model = Restaurant
        fields = ['name', 'cnpj', 'phone', 'email', 'website', 'description', 'admin_email', 'admin_first_name', 'admin_last_name']
        # Add other fields from Restaurant as needed

    def save(self, commit=True):
        restaurant = super().save(commit=False)

        admin_email = self.cleaned_data.get('admin_email')
        admin_first_name = self.cleaned_data.get('admin_first_name')
        admin_last_name = self.cleaned_data.get('admin_last_name')

        if admin_email:
            admin_user, created = CustomUser.objects.get_or_create(email=admin_email)
            admin_user.first_name = admin_first_name
            admin_user.last_name = admin_last_name
            admin_user.is_staff = True
            admin_user.save()
            restaurant.admin = admin_user

        if commit:
            restaurant.save()
        return restaurant