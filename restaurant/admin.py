from django.contrib import admin
from .models import Restaurant
from custom_auth.models import CustomUser

class CustomUserInline(admin.StackedInline):
    model = CustomUser
    can_delete = False
    verbose_name_plural = 'Users'
    fk_name = 'restaurant'

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    inlines = (CustomUserInline,)
    list_display = ('name',)
    search_fields = ('name',)