from django.contrib import admin
from .models import (
    Restaurant, RestaurantUnit, WorkingHours,
    BlockedHours, RestaurantCategory, CuisineType
)
from custom_auth.models import CustomUser
from address.models import Address

class CustomUserInline(admin.StackedInline):
    model = CustomUser
    can_delete = False
    verbose_name_plural = 'Users'
    fk_name = 'restaurant'
    
class AddressInline(admin.TabularInline):
    model = Address
    extra = 1
    readonly_fields = ('address_id',)

class WorkingHoursInline(admin.TabularInline):
    model = WorkingHours
    extra = 1

class BlockedHoursInline(admin.TabularInline):
    model = BlockedHours
    extra = 1

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    inlines = (CustomUserInline, AddressInline,)
    list_display = ('name', 'cnpj', 'email', 'category')
    search_fields = ('name', 'cnpj', 'email')
    list_filter = ('category', 'cuisine_types')

    fieldsets = (
        (None, {
            'fields': (
                'name', 'cnpj', 'country_code', 'phone', 'email',
                'website', 'description', 'image', 'role', 'admin',
                'category', 'cuisine_types'
            )
        }),
        ('Important Dates', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('cuisine_types', 'customers', 'employees', 'login_logs')

@admin.register(RestaurantUnit)
class RestaurantUnitAdmin(admin.ModelAdmin):
    inlines = (WorkingHoursInline, BlockedHoursInline)
    list_display = ('name', 'restaurant', 'is_main_unit')
    search_fields = ('name', 'restaurant__name')
    list_filter = ('is_main_unit',)

admin.site.register(RestaurantCategory)
admin.site.register(CuisineType)