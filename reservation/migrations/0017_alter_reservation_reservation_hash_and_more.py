# Generated by Django 5.0.9 on 2024-12-27 01:04

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0016_alter_reservation_reservation_hash'),
        ('restaurant', '0007_restaurantemployee_country_code'),
        ('restaurant_customer', '0005_remove_restaurantcustomer_restaurant__name_78fb79_idx_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='reservation_hash',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AddIndex(
            model_name='reservation',
            index=models.Index(fields=['reserver', 'start_time', 'end_time', 'reservation_date', 'reservation_hash'], name='reservation_idx'),
        ),
    ]
