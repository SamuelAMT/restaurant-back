from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('reserver', 'date', 'time', 'amount_of_people')
    search_fields = ('reserver', 'reservation_hash')
    list_filter = ('date', 'time')
    readonly_fields = ('reservation_hash', 'status')
    
    exclude = ()

    def get_exclude(self, request, obj=None):
        if not obj:
            return ('status',)
        return ()
    
    def save_model(self, request, obj, form, change):
        if not obj.restaurant:
            # Set the restaurant based on the admin user's associated restaurant
            obj.restaurant = request.user.restaurant
        super().save_model(request, obj, form, change)