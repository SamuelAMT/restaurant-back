from django.db import models

class Role(models.TextChoices):
    RESTAURANTCUSTOMER = "RESTAURANTCUSTOMER", "RestaurantCustomer"
    ADMIN = "ADMIN", "Admin"
    RESTAURANT = "RESTAURANT", "Restaurant"
    RESTAURANTEMPLOYEE = "RESTAURANTEMPLOYEE", "RestaurantEmployee"

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
        'restaurant.Restaurant',
        on_delete=models.CASCADE,
        related_name="accounts",
        null=True,
        blank=True,
    )
    employee = models.ForeignKey(
        'restaurant.RestaurantEmployee', 
        on_delete=models.CASCADE,
        related_name="accounts",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Account {self.provider} - {self.provider_account_id}"

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

class Session(models.Model):
    session_token = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(
        'restaurant.Restaurant',
        on_delete=models.CASCADE,
        related_name="sessions"
    )
    expires = models.DateTimeField()

    def __str__(self):
        return f"Session {self.session_token}"

    class Meta:
        indexes = [
            models.Index(fields=["session_token"], name="session_token_idx"),
            models.Index(fields=["expires"], name="expires_idx"),
        ]
        verbose_name = "Session"
        verbose_name_plural = "Sessions"

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
