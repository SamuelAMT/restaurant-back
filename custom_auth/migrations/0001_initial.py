# Generated by Django 5.0.8 on 2024-10-22 22:38

import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('account_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('type', models.CharField(max_length=50)),
                ('provider', models.CharField(max_length=50)),
                ('provider_account_id', models.CharField(max_length=100)),
                ('refresh_token', models.CharField(blank=True, max_length=200, null=True)),
                ('access_token', models.CharField(blank=True, max_length=200, null=True)),
                ('expires_at', models.IntegerField(blank=True, null=True)),
                ('token_type', models.CharField(blank=True, max_length=50, null=True)),
                ('scope', models.CharField(blank=True, max_length=100, null=True)),
                ('id_token', models.CharField(blank=True, max_length=500, null=True)),
                ('session_state', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('custom_user_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('role', models.CharField(choices=[('RESTAURANTCUSTOMER', 'RestaurantCustomer'), ('ADMIN', 'Admin'), ('RESTAURANT', 'Restaurant'), ('RESTAURANTEMPLOYEE', 'RestaurantEmployee')], default='RESTAURANTEMPLOYEE', max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LoginLog',
            fields=[
                ('login_log_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('ip_address', models.GenericIPAddressField(default='0.0.0.0')),
                ('user_agent', models.TextField(default='Unknown')),
                ('action', models.CharField(default='login', max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('session_token', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('ip_address', models.GenericIPAddressField(default='0.0.0.0')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_active_at', models.DateTimeField(auto_now=True)),
                ('is_expired', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Session',
                'verbose_name_plural': 'Sessions',
            },
        ),
        migrations.CreateModel(
            name='VerificationToken',
            fields=[
                ('token', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('expires', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Verification Token',
                'verbose_name_plural': 'Verification Tokens',
            },
        ),
    ]
