from django.contrib import admin
from .models import RestaurantCustomer

@admin.register(RestaurantCustomer)
class RestaurantCustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    exclude = ()

    def get_exclude(self, request, obj=None):
        if not obj:
            return ('status',)
        return ()