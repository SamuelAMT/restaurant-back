from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
    Permission,
)

from django.db import models
from django.utils import timezone
import uuid


class Role(models.TextChoices):
    RESTAURANTCUSTOMER = "RESTAURANTCUSTOMER", "RestaurantCustomer"
    ADMIN = "ADMIN", "Admin"
    RESTAURANT = "RESTAURANT", "Restaurant"
    RESTAURANTEMPLOYEE = "RESTAURANTEMPLOYEE", "RestaurantEmployee"


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(models.Model):
    account_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    type = models.CharField(max_length=50)
    provider = models.CharField(max_length=50)
    provider_account_id = models.CharField(max_length=100)
    refresh_token = models.CharField(max_length=200, null=True, blank=True)
    access_token = models.CharField(max_length=200, null=True, blank=True)
    expires_at = models.IntegerField(null=True, blank=True)
    token_type = models.CharField(max_length=50, null=True, blank=True)
    scope = models.CharField(max_length=100, null=True, blank=True)
    id_token = models.CharField(max_length=500, null=True, blank=True)
    session_state = models.CharField(max_length=100, null=True, blank=True)

    restaurant = models.ForeignKey(
        "restaurant.Restaurant",
        on_delete=models.CASCADE,
        related_name="auth_accounts",
        null=True,
        blank=True,
    )
    employee = models.ForeignKey(
        "restaurant.RestaurantEmployee",
        on_delete=models.CASCADE,
        related_name="staff_accounts",
        null=True,
        blank=True,
    )

    email = models.EmailField(unique=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_system_account = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"

    objects = AccountManager()

    def __str__(self):
        return self.email or f"Account {self.provider} - {self.provider_account_id}"

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        indexes = [
            models.Index(
                fields=["provider", "provider_account_id"], name="provider_account_idx"
            ),
            models.Index(fields=["access_token"], name="access_token_idx"),
            models.Index(fields=["expires_at"], name="expires_at_idx"),
        ]
        verbose_name = "Account"
        verbose_name_plural = "Accounts"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        #extra_fields.setdefault("role", Role.RESTAURANTEMPLOYEE)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", Role.ADMIN)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    custom_user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(
        max_length=50, choices=Role.choices, default=Role.RESTAURANTEMPLOYEE
    )

    groups = models.ManyToManyField(
        Group,
        related_name="customeruser_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customeruser_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class VerificationToken(models.Model):
    token = models.CharField(max_length=100, primary_key=True, unique=True)
    expires = models.DateTimeField()

    def __str__(self):
        return f"Token for {self.token}"

    class Meta:
        indexes = [
            models.Index(fields=["token"], name="token_idx"),
        ]
        verbose_name = "Verification Token"
        verbose_name_plural = "Verification Tokens"


class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500, unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token

    class Meta:
        verbose_name = "Blacklisted Token"
        verbose_name_plural = "Blacklisted Tokens"


def get_default_account():
    default_account_id = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
    try:
        return Account.objects.get(account_id=default_account_id).pk
    except Account.DoesNotExist:
        raise ValueError(
            "System account does not exist. Please create a system account with the specified UUID."
        )


class LoginLog(models.Model):
    login_log_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=False, default=get_default_account
    )
    ip_address = models.GenericIPAddressField(default="0.0.0.0")
    user_agent = models.TextField(default="Unknown")
    action = models.CharField(max_length=50, default="login")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action.capitalize()} log for {self.account.email} on {self.timestamp}"
