from django.contrib import admin
from .models import CustomUser, Role, LoginLog, VerificationToken
#from .models import Account 
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

#@admin.register(Account)
#class AccountAdmin(admin.ModelAdmin):
#    list_display = ('email', 'is_admin', 'is_active', 'created_at')
#    list_filter = ('is_admin', 'is_active', 'created_at')
#    search_fields = ('email',)
#    ordering = ('-created_at',)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('email', 'first_name', 'last_name', 'role', 'restaurant', 'is_active', 'is_staff')
    list_filter = ('role', 'restaurant', 'is_active', 'is_staff', 'is_superuser', 'groups')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Roles and Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Restaurant', {'fields': ('restaurant',)}),
        ('Important Dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    list_display = ('custom_user', 'action', 'ip_address', 'timestamp')
    list_filter = ('action', 'timestamp')

@admin.register(VerificationToken)
class VerificationTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'expires')