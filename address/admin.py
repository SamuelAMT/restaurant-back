from django.contrib import admin
from .models import Address
from .forms import AddressForm

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    form = AddressForm
    
    list_display = (
        'address_id',
        'restaurant',
        'cep', 
        'street', 
        'number', 
        'neighborhood', 
        'city', 
        'state', 
        'country'
    )
    
    search_fields = (
        'street', 
        'city', 
        'state',
        'restaurant__name',  # Allow searching by restaurant name
        'address_id'
    )
    
    list_filter = (
        'created_at',
        'state',
        'country',
        'restaurant'
    )
    
    readonly_fields = (
        'created_at', 
        'updated_at',
        'address_id'
    )

    fieldsets = (
        ('Restaurant Information', {
            'fields': ('restaurant', 'address_id')
        }),
        ('Address Details', {
            'fields': (
                'cep',
                'street',
                'number',
                'neighborhood',
                'city',
                'state',
                'country',
                'complement'
            )
        }),
        ('Important Dates', {
            'fields': ('created_at', 'updated_at'),
        })
    )

    def save_model(self, request, obj, form, change):
        if not obj.restaurant and hasattr(request.user, 'restaurant'):
            obj.restaurant = request.user.restaurant
        super().save_model(request, obj, form, change)