# Generated by Django 5.0.8 on 2024-10-22 03:07

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
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='restaurant_customer.restaurantcustomer'),
        ),
        migrations.AddField(
            model_name='restaurantvisit',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant_visits', to='restaurant.restaurant'),
        ),
        migrations.AddField(
            model_name='restaurantvisit',
            name='restaurant_customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='restaurant_visits', to='restaurant_customer.restaurantcustomer'),
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
