# Generated by Django 5.0.8 on 2024-10-22 03:07

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantCustomer',
            fields=[
                ('restaurant_customer_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('lastname', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=70, unique=True)),
                ('country_code', models.CharField(blank=True, max_length=3, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reservations', models.ManyToManyField(related_name='restaurant_customers', to='reservation.reservation')),
            ],
            options={
                'indexes': [models.Index(fields=['name', 'lastname', 'phone'], name='restaurant__name_78fb79_idx')],
            },
        ),
    ]
