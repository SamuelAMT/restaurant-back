from django.contrib import admin
from .models import Reservation
from restaurant.models import Restaurant


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    def customer_email(self, obj):
        return obj.customer.email if obj.customer else None

    customer_email.short_description = "Customer Email"

    list_display = ("reserver", "date", "start_time", "end_time", "amount_of_people")
    search_fields = ("reserver", "reservation_hash", "email")
    list_filter = (
        "date",
        "start_time",
        "end_time",
    )
    readonly_fields = ("reservation_hash", "status", "customer")

    exclude = ("customer",)

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
                    "phone": obj.phone,
                    "birthday": obj.birthday,
                    "country_code": obj.country_code,
                },
            )
            obj.customer = customer

        super().save_model(request, obj, form, change)
