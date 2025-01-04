# Generated by Django 5.0.9 on 2025-01-04 03:02

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('unit_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('is_main_unit', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to='restaurant.restaurant')),
            ],
            options={
                'db_table': 'restaurant_unit',
                'unique_together': {('restaurant', 'name')},
            },
        ),
        migrations.CreateModel(
            name='BlockedHours',
            fields=[
                ('blocked_hours_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
                ('reason', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_hours', to='unit.unit')),
            ],
            options={
                'db_table': 'blocked_hours',
                'ordering': ['-start_datetime'],
            },
        ),
        migrations.CreateModel(
            name='WorkingHours',
            fields=[
                ('working_hours_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('day_of_week', models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')])),
                ('opening_time', models.TimeField()),
                ('closing_time', models.TimeField()),
                ('is_closed', models.BooleanField(default=False)),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='working_hours', to='unit.unit')),
            ],
            options={
                'db_table': 'working_hours',
                'unique_together': {('unit', 'day_of_week')},
            },
        ),
    ]
