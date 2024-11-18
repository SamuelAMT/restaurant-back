from django.contrib import admin
from .models import Restaurant
from custom_auth.models import CustomUser
from address.models import Address
from django.core.exceptions import ValidationError

class CustomUserInline(admin.StackedInline):
    model = CustomUser
    can_delete = False
    verbose_name_plural = 'Users'
    fk_name = 'restaurant'
    
class AddressInline(admin.TabularInline):
    model = Address
    extra = 1
    readonly_fields = ('address_id',)

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    inlines = (CustomUserInline, AddressInline,)
    list_display = ('name', 'cnpj', 'email')
    search_fields = ('name', 'cnpj', 'email')

    fieldsets = (
        (None, {
            'fields': (
                'name', 'cnpj', 'country_code', 'phone', 'email', 'website',
                'description', 'image', 'role', 'admin',
            )
        }),
        ('Important Dates', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    filter_horizontal = ('customers', 'employees', 'login_logs')