from django.db import models

# Create your models here.

class Restaurant(models.Model):
    # Implement inheritance or increment address
    # and it's fields as a parameter to Restaurant
    cnpj = models.CharField(max_length=14, primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=70, blank=True, null=True)
    # default="default@example.com"
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='restaurant/images', blank=True, null=True)
    def __str__(self):
        return self.name