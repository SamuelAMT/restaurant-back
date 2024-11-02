from django.contrib import admin
from .models import Account, CustomUser, Role, Session, LoginLog, VerificationToken, BlacklistedToken

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_admin', 'is_active', 'created_at')
    list_filter = ('is_admin', 'is_active', 'created_at')
    search_fields = ('email',)
    ordering = ('-created_at',)

@admin.register(CustomUser) 
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('email',)

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('account', 'created_at', 'expires', 'is_expired')
    list_filter = ('is_expired', 'created_at')

@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    list_display = ('account', 'action', 'ip_address', 'timestamp')
    list_filter = ('action', 'timestamp')

@admin.register(VerificationToken)
class VerificationTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'expires')
    
@admin.register(BlacklistedToken)
class BlacklistedTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'blacklisted_at')