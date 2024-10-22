from django.contrib import admin
from .models import Account, Session, LoginLog

class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'created_at')
    search_fields = ('email',)

class SessionAdmin(admin.ModelAdmin):
    list_display = ('account', 'session_token', 'ip_address', 'created_at', 'expires', 'last_active_at', 'is_expired')
    search_fields = ('account__email', 'session_key')

class LoginLogAdmin(admin.ModelAdmin):
    list_display = ('account', 'action', 'ip_address', 'timestamp')
    search_fields = ('account__email', 'action', 'ip_address')

admin.site.register(Account, AccountAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(LoginLog, LoginLogAdmin)
