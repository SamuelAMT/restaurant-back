from django.contrib import admin
from .models import Address
from .forms import AddressForm

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    form = AddressForm
    
    list_display = (
        'address_id',
        'get_unit',
        'get_restaurant',
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
        'unit__name',
        'unit__restaurant__name',
        'address_id'
    )
    
    list_filter = (
        'created_at',
        'state',
        'country',
    )
    
    readonly_fields = (
        'created_at', 
        'updated_at',
        'address_id'
    )

    fieldsets = (
        ('Restaurant Information', {
            'fields': ('unit', 'address_id')
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

    def get_unit(self, obj):
        """Get the associated unit"""
        return obj.unit.name if hasattr(obj, 'unit') else None
    get_unit.short_description = 'Unit'
    get_unit.admin_order_field = 'unit__name'

    def get_restaurant(self, obj):
        """Get the restaurant through the unit relationship"""
        if hasattr(obj, 'unit') and obj.unit:
            return obj.unit.restaurant
        return None
    get_restaurant.short_description = 'Restaurant'
    get_restaurant.admin_order_field = 'unit__restaurant'