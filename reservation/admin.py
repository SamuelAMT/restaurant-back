from django.contrib import admin
from .models import Reservation
from .forms import ReservationForm

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    form = ReservationForm
    
    def customer_email(self, obj):
        return obj.customer.email if obj.customer else None
    
    customer_email.short_description = "Customer Email"
    
    list_display = (
        "reserver",
        "unit",
        "reservation_date",
        "start_time",
        "end_time",
        "amount_of_people",
        "amount_of_hours",
        "status"
    )
    
    search_fields = (
        "reserver",
        "reservation_hash",
        "email",
        "observation"
        "unit__name",
        "restaurant_name",
    )
    
    list_filter = (
        "reservation_date",
        "start_time",
        "end_time",
        "status",
        "unit",
        "restaurant",
    )
    
    readonly_fields = (
        "reservation_hash",
        "status",
        "customer",
        "created_at",
        "amount_of_hours",
        "restaurant",
    )

    exclude = ("customer",)

    fieldsets = (
        (None, {
            'fields': (
                'reserver',
                'unit',
                'restaurant',
                'reservation_date',
                'start_time',
                'end_time',
                'amount_of_people',
                'amount_of_hours',
                'email',
                'country_code',
                'phone',
                'birthday',
            )
        }),
        ('Additional Information', {
            'fields': (
                'observation',
                'status',
                'reservation_hash',
            )
        }),
        ('Dates', {
            'fields': ('created_at',),
        })
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.restaurant and obj.unit:
            obj.restaurant = obj.unit.restaurant
        super().save_model(request, obj, form, change)