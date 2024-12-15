# Generated by Django 5.0.9 on 2024-11-27 02:21

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='reservation_hash',
            field=models.CharField(db_index=True, default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('canceled', 'Canceled')], default='pending', max_length=20),
        ),
    ]
