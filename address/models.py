from django.db import models
import uuid
from django.utils import timezone
from django.core.validators import RegexValidator
from unit.models import Unit

class Address(models.Model):
    address_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    cep = models.CharField(
        max_length=9,
        validators=[
            RegexValidator(
                regex=r"^\d{5}-?\d{3}$", message="CEP must be in the format 00000-000"
            )
        ],
    )
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    neighborhood = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    country = models.CharField(max_length=50)
    complement = models.CharField(max_length=100, null=True, blank=True)
    maps_url = models.URLField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(null=False, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    unit = models.OneToOneField(
        Unit,
        on_delete=models.CASCADE,
        related_name='address',
        null=True,
        db_column='unit_id'
    )

    class Meta:
        unique_together = (
            ("cep", "street", "number", "neighborhood", "city", "state", "country"),
        )
        indexes = [
            models.Index(fields=['address_id'], name='address_address_e701d2_idx'),
            models.Index(fields=['cep'], name='address_cep_a6f9b0_idx'),
            models.Index(fields=['city', 'state'], name='address_city_daed79_idx')
        ]
        db_table = "address"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.street}, {self.number} - {self.neighborhood}, {self.city}/{self.state}"

    def clean(self):
        """Clean and format CEP"""
        if self.cep:
            self.cep = self.cep.replace("-", "")