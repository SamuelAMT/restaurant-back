from django.contrib import admin
from .models import Reservation
from .forms import ReservationForm
from restaurant.models import Restaurant

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    form = ReservationForm

    def customer_email(self, obj):
        return obj.customer.email if obj.customer else None

    customer_email.short_description = "Customer Email"

    list_display = (
        "reserver",
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
    )
    
    list_filter = (
        "reservation_date",
        "start_time",
        "end_time",
        "status"
    )
    
    readonly_fields = (
        "reservation_hash",
        "status",
        "customer",
        "created_at",
        "amount_of_hours"
    )

    exclude = ("customer",)

    fieldsets = (
        (None, {
            'fields': (
                'reserver',
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
                'restaurant',
                'status',
                'reservation_hash',
            )
        }),
        ('Dates', {
            'fields': ('created_at',),
        })
    )

    def save_model(self, request, obj, form, change):
        if not obj.restaurant:
            obj.restaurant = request.user.restaurant

        if obj.email:
            from restaurant_customer.models import RestaurantCustomer
            customer, created = RestaurantCustomer.objects.get_or_create(
                email=obj.email,
                defaults={
                    "name": obj.reserver,
                    "lastname": "",
                    "country_code": obj.country_code,
                    "phone": obj.phone,
                    "birthday": obj.birthday,
                },
            )
            obj.customer = customer

        super().save_model(request, obj, form, change)