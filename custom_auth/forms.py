from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, LoginLog, VerificationToken


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
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
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["autofocus"] = True
        self.fields["email"].required = True
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "role",
            "restaurant",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True


class LoginLogForm(forms.ModelForm):
    class Meta:
        model = LoginLog
        fields = ("custom_user", "action", "ip_address")


class VerificationTokenForm(forms.ModelForm):
    class Meta:
        model = VerificationToken
        fields = ("token", "expires")
        widgets = {"expires": forms.DateTimeInput()}
