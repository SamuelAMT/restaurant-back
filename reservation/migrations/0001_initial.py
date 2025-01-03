# Generated by Django 5.0.9 on 2025-01-03 01:10

import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('reservation_hash', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('reserver', models.CharField(db_index=True, max_length=100)),
                ('amount_of_people', models.PositiveIntegerField()),
                ('amount_of_hours', models.PositiveIntegerField()),
                ('start_time', models.TimeField(db_index=True)),
                ('end_time', models.TimeField(db_index=True)),
                ('reservation_date', models.DateField(db_index=True)),
                ('email', models.EmailField(max_length=70)),
                ('country_code', models.CharField(blank=True, max_length=3, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('observation', models.TextField(blank=True, max_length=250, null=True)),
                ('status', models.CharField(choices=[('confirmed', 'Confirmed'), ('canceled', 'Canceled'), ('finished', 'Finished')], default='confirmed', max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'reservation',
            },
        ),
    ]
