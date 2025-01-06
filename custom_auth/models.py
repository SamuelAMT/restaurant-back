from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
    Permission,
)

from django.db import models
from django.conf import settings
import uuid
from django.utils import timezone
from django.core.exceptions import ValidationError


class Role(models.TextChoices):
    SUPERADMIN = "SUPERADMIN", "Super Admin"
    RESTAURANT_ADMIN = "RESTAURANT_ADMIN", "Restaurant Administrator"
    UNIT_ADMIN = "UNIT_ADMIN", "Unit Administrator"
    UNIT_SUB_ADMIN = "UNIT_SUB_ADMIN", "Unit Sub Administrator"
    UNIT_STAFF = "UNIT_STAFF", "Unit Staff"


class CustomUserManager(BaseUserManager):
    def create_user(
        self, email, password=None, role=Role.UNIT_STAFF, **extra_fields
    ):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_restaurant_admin(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        return self.create_user(
            email, password, role=Role.RESTAURANT_ADMIN, **extra_fields
        )

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, role=Role.SUPERADMIN, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    custom_user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.UNIT_STAFF
    )
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=False, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    restaurant = models.ForeignKey(
        "restaurant.Restaurant",
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True,
    )

    unit = models.ForeignKey(
        "unit.Unit",
        on_delete=models.CASCADE,
        related_name="unit_users",
        null=True,
        blank=True,
    )

    groups = models.ManyToManyField(
        Group,
        blank=True,
        help_text="The groups this user belongs to.",
        related_name="customeruser_set",
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
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        indexes = [
            models.Index(
                fields=["custom_user_id", "email"], name="custom_user__id_email_idx"
            )
        ]
        db_table = "custom_user"

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        if self.role == Role.RESTAURANT_ADMIN and self.restaurant is None:
            raise ValidationError(
                "Restaurant Admin must be associated with a restaurant"
            )
        if self.role in [Role.UNIT_ADMIN, Role.UNIT_SUB_ADMIN, Role.UNIT_STAFF]:
            if self.unit is None:
                raise ValidationError("Unit-based roles must be associated with a unit")
            if self.restaurant is None:
                raise ValidationError(
                    "Unit-based roles must be associated with a restaurant"
                )


class VerificationToken(models.Model):
    token = models.CharField(max_length=100, primary_key=True, unique=True)
    expires = models.DateTimeField()

    def __str__(self):
        return f"Token for {self.token}"

    class Meta:
        indexes = [
            models.Index(fields=["token"], name="token_idx"),
        ]
        db_table = "verification_token"
        verbose_name = "Verification Token"
        verbose_name_plural = "Verification Tokens"


class LoginLog(models.Model):
    login_log_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    custom_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    ip_address = models.GenericIPAddressField(default="0.0.0.0")
    user_agent = models.TextField(default="Unknown")
    action = models.CharField(max_length=50, default="login")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "login_log"

    def __str__(self):
        return f"{self.action.capitalize()} log for {self.custom_user.email} on {self.timestamp}"
