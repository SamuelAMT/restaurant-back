# Generated by Django 5.0.9 on 2024-12-27 05:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0009_populate_unit_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantemployee',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='restaurant.restaurantunit'),
        ),
    ]