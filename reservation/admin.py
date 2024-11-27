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