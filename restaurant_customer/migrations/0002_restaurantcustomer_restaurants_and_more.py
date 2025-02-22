# Generated by Django 5.0.9 on 2025-01-10 23:24

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_initial'),
        ('restaurant_customer', '0001_initial'),
        ('unit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurantcustomer',
            name='restaurants',
            field=models.ManyToManyField(blank=True, related_name='customer_restaurants', to='restaurant.restaurant'),
        ),
        migrations.AlterField(
            model_name='restaurantcustomer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='restaurantcustomer',
            name='first_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='restaurantcustomer',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='restaurantcustomer',
            name='restaurant_customer_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='restaurantcustomer',
            name='units',
            field=models.ManyToManyField(related_name='customer_units', to='unit.unit'),
        ),
    ]
