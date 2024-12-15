from django.db import models

class Address(models.Model):
    address_id = models.AutoField(primary_key=True, db_index=True)
    cep = models.CharField(max_length=9)
    street = models.CharField(max_length=30)
    number = models.CharField(max_length=10)
    neighborhood = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    country = models.CharField(max_length=30)
    complement = models.CharField(max_length=100, null=True, blank=True)

    restaurant = models.ForeignKey(
        "restaurant.Restaurant",
        on_delete=models.CASCADE,
        related_name='addresses',
        null=False,
    )

    class Meta:
        unique_together = (('cep', 'street', 'number', 'neighborhood', 'city', 'state', 'country'),)
        indexes = [models.Index(fields=['address_id'])]
        db_table = 'address'

    def __str__(self):
        return f"{self.address_id} - {self.cep}, {self.street}, {self.number} - {self.neighborhood}, {self.city} - {self.state} - {self.country}"
