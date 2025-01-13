from django.contrib import admin
from django.contrib import messages
from django.db import transaction
from .models import RestaurantCustomer
from .forms import RestaurantCustomerForm

@admin.register(RestaurantCustomer)
class RestaurantCustomerAdmin(admin.ModelAdmin):
    form = RestaurantCustomerForm

    list_display = (
        'restaurant_customer_id',
        'get_restaurant_names',
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
        ('Restaurant Information', {
            'fields': (
                'restaurants',
            )
        }),
        ('Important Dates', {
            'fields': ('created_at', 'updated_at'),
        })
    )

    filter_horizontal = ('units', 'restaurants')  # Add filter_horizontal for units and restaurants

    def save_model(self, request, obj, form, change):
        try:
            with transaction.atomic():
                super().save_model(request, obj, form, change)

                units = form.cleaned_data.get('units', [])

                obj.units.set(units)

                unit_restaurants = {unit.restaurant for unit in units if unit.restaurant}

                if hasattr(request.user, 'restaurant') and request.user.restaurant:
                    unit_restaurants.add(request.user.restaurant)

                # Ensure at least one restaurant is associated
                if not unit_restaurants:
                    raise ValueError("No restaurants found for the selected units.")

                obj.restaurants.set(unit_restaurants)

                messages.success(request, f'Restaurant customer "{obj}" was saved successfully.')
        except Exception as e:
            messages.error(request, f'Error saving restaurant customer: {str(e)}')
            raise

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'restaurant'):
            return qs.filter(restaurants=request.user.restaurant)
        return qs

    def get_restaurant_names(self, obj):
        return ", ".join([restaurant.name for restaurant in obj.restaurants.all()])

    get_restaurant_names.short_description = 'Restaurants'