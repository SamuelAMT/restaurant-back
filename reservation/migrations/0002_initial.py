# Generated by Django 5.0.9 on 2024-11-12 03:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reservation', '0001_initial'),
        ('restaurant', '0001_initial'),
        ('restaurant_customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_reservations', to='restaurant_customer.restaurantcustomer'),
        ),
        migrations.AddField(
            model_name='restaurantvisit',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='restaurant_customer.restaurantcustomer'),
        ),
        migrations.AddField(
            model_name='restaurantvisit',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='restaurant.restaurant'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='visit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='reservation.restaurantvisit'),
        ),
        migrations.AddIndex(
            model_name='reservation',
            index=models.Index(fields=['reserver', 'time', 'date', 'reservation_hash'], name='reservation_reserve_9df32c_idx'),
        ),
    ]
