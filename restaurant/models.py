from django.db import models

class Restaurant(models.Model):
    cnpj = models.CharField(max_length=14, primary_key=True, db_index=True)
    name = models.CharField(max_length=100, db_index=True)
    country_code = models.CharField(max_length=3, blank=False, null=False)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=70, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)

    customers = models.ManyToManyField(
        'restaurant_customer.RestaurantCustomer',
        related_name='restaurants'
    )
    
    class Meta:
        indexes = [models.Index(fields=['cnpj', 'name'], name='restaurant__cnpj_8b2fef_idx')]

    def __str__(self):
        return self.name
