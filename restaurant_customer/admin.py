from django.contrib import admin
from django.contrib import messages
from .models import RestaurantCustomer
from .forms import RestaurantCustomerForm


@admin.register(RestaurantCustomer)
class RestaurantCustomerAdmin(admin.ModelAdmin):
    form = RestaurantCustomerForm

    list_display = (
        'restaurant_customer_id',
        'get_restaurant_names',
        'get_unit_names',
        'first_name',
        'last_name',
        'email',
        'country_code',
        'phone',
        'birthday'
    )

    search_fields = (
        'first_name',
        'last_name',
        'email',
        'phone',
        'restaurants__name',
        'units__name',
        'restaurant_customer_id'
    )

    list_filter = (
        'created_at',
        'units',
        'country_code'
    )

    readonly_fields = (
        'created_at',
        'updated_at',
        'restaurant_customer_id'
    )

    fieldsets = (
        ('Personal Information', {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'country_code',
                'phone',
                'birthday'
            )
        }),
        ('Unit Information', {
            'fields': (
                'units',
            )
        }),
        ('Important Dates', {
            'fields': ('created_at', 'updated_at'),
        })
    )

    def get_unit_names(self, obj):
        return ", ".join([unit.name for unit in obj.units.all()])

    get_unit_names.short_description = 'Units'

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)

            # Get restaurants from the selected units
            unit_restaurants = {unit.restaurant for unit in obj.units.all()}

            # If user is a restaurant admin, ensure their restaurant is included
            if hasattr(request.user, 'restaurant'):
                unit_restaurants.add(request.user.restaurant)

            obj.restaurants.set(unit_restaurants)

            messages.success(request, f'Restaurant customer "{obj}" was saved successfully.')
        except Exception as e:
            messages.error(request, f'Error saving restaurant customer: {str(e)}')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'restaurant'):
            return qs.filter(restaurants=request.user.restaurant)
        return qs

    def get_restaurant_names(self, obj):
        return ", ".join([restaurant.name for restaurant in obj.restaurants.all()])

    get_restaurant_names.short_description = 'Restaurants'