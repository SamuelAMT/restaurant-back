from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from .models import Account
from .models import CustomUser, LoginLog, VerificationToken
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    LoginLogForm,
    VerificationTokenForm,
)

# @admin.register(Account)
# class AccountAdmin(admin.ModelAdmin):
#    list_display = ('email', 'is_admin', 'is_active', 'created_at')
#    list_filter = ('is_admin', 'is_active', 'created_at')
#    search_fields = ('email',)
#    ordering = ('created_at',)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = CustomUser

    list_display = (
        "email",
        "first_name",
        "last_name",
        "role",
        "restaurant",
        "is_active",
        "is_staff",
        "last_login",
    )

    list_filter = (
        "role",
        "restaurant",
        "is_active",
        "is_staff",
        "is_superuser",
        "groups",
        "last_login",
    )

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        (
            "Roles and Permissions",
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Restaurant", {"fields": ("restaurant",)}),
        ("Important Dates", {"fields": ("last_login",), "classes": ("collapse",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "role",
                    "restaurant",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    search_fields = ("email", "first_name", "last_name", "restaurant__name")
    ordering = ("email",)
    filter_horizontal = ("groups", "user_permissions")


@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    form = LoginLogForm
    list_display = ("custom_user", "action", "ip_address", "timestamp")
    list_filter = ("action", "timestamp")
    search_fields = ("custom_user__email", "ip_address")
    readonly_fields = ("timestamp",)


@admin.register(VerificationToken)
class VerificationTokenAdmin(admin.ModelAdmin):
    form = VerificationTokenForm
    list_display = ("token", "expires")
    search_fields = ("token",)
    readonly_fields = ("token",)
