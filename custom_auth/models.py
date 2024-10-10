from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class Role(models.TextChoices):
    RESTAURANTCUSTOMER = "RESTAURANTCUSTOMER", "RestaurantCustomer"
    ADMIN = "ADMIN", "Admin"
    RESTAURANT = "RESTAURANT", "Restaurant"
    RESTAURANTEMPLOYEE = "RESTAURANTEMPLOYEE", "RestaurantEmployee"


class Admin(BaseUserManager):
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
        related_name="accounts",
        null=True,
        blank=True,
    )
    employee = models.ForeignKey(
        "restaurant.RestaurantEmployee",
        on_delete=models.CASCADE,
        related_name="accounts",
        null=True,
        blank=True,
    )

    email = models.EmailField(unique=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"

    objects = Admin()

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


class VerificationToken(models.Model):
    identifier = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    expires = models.DateTimeField()

    def __str__(self):
        return f"Token for {self.identifier}"

    class Meta:
        indexes = [
            models.Index(fields=["identifier"], name="identifier_idx"),
            models.Index(fields=["token"], name="token_idx"),
        ]
        verbose_name = "Verification Token"
        verbose_name_plural = "Verification Tokens"


class LoginLog(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    action = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action.capitalize()} log for {self.account.email} on {self.timestamp}"
