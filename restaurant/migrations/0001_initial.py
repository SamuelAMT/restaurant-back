# Generated by Django 5.0.9 on 2024-11-12 03:03

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0001_initial'),
        ('custom_auth', '0001_initial'),
        ('restaurant_customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('restaurant_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('cnpj', models.CharField(db_index=True, max_length=14, unique=True)),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('country_code', models.CharField(max_length=3)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(blank=True, max_length=70, null=True)),
                ('email_verified', models.EmailField(blank=True, max_length=254, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.URLField(blank=True, null=True)),
                ('role', models.CharField(choices=[('RESTAURANTCUSTOMER', 'RestaurantCustomer'), ('ADMIN', 'Admin'), ('RESTAURANT_ADMIN', 'Restaurant Admin'), ('RESTAURANT_STAFF', 'Restaurant Staff')], default='RESTAURANT_ADMIN', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('addresses', models.ManyToManyField(related_name='restaurants', to='address.address')),
                ('customers', models.ManyToManyField(related_name='restaurants', to='restaurant_customer.restaurantcustomer')),
                ('login_logs', models.ManyToManyField(related_name='restaurants', to='custom_auth.loginlog')),
            ],
        ),
        migrations.CreateModel(
            name='RestaurantEmployee',
            fields=[
                ('restaurant_employee_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=70, unique=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('role', models.CharField(choices=[('RESTAURANTCUSTOMER', 'RestaurantCustomer'), ('ADMIN', 'Admin'), ('RESTAURANT_ADMIN', 'Restaurant Admin'), ('RESTAURANT_STAFF', 'Restaurant Staff')], default='RESTAURANT_STAFF', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff', to='restaurant.restaurant')),
            ],
        ),
        migrations.AddField(
            model_name='restaurant',
            name='employees',
            field=models.ManyToManyField(related_name='restaurants', to='restaurant.restaurantemployee'),
        ),
        migrations.AddIndex(
            model_name='restaurant',
            index=models.Index(fields=['restaurant_id', 'name'], name='restaurant__id_name_idx'),
        ),
    ]
