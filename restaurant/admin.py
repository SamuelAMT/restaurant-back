from django.contrib import admin
from .models import (
    Restaurant, RestaurantCategory, CuisineType
)
from unit.models.unit import Unit
from unit.api.schemas.schedule import WorkingHoursSchema, BlockedHoursSchema
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

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    inlines = (CustomUserInline,)
    list_display = ('name', 'cnpj', 'email', 'category', 'get_unit_count')
    search_fields = ('name', 'cnpj', 'email', 'get_unit_count')
    list_filter = ('category', 'cuisine_types', 'created_at')

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name', 
                'cnpj', 
                'category',
                'cuisine_types'
            )
        }),
        ('Contact Information', {
            'fields': (
                'country_code',
                'phone',
                'email',
                'website'
            )
        }),
        ('Details', {
            'fields': (
                'description',
                'image',
                'role',
                'admin'
            )
        }),
        ('Important Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('cuisine_types', 'customers', 'employees', 'login_logs')
    
    def get_unit_count(self, obj):
        return obj.units.count()
    get_unit_count.short_description = 'Number of Units'

@admin.register(RestaurantCategory)
class RestaurantCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(CuisineType)
class CuisineTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Unit)
class RestaurantUnitAdmin(admin.ModelAdmin):
    inlines = ()
    list_display = ('name', 'restaurant', 'is_main_unit')
    search_fields = ('name', 'restaurant__name',)
    list_filter = ('is_main_unit',)
