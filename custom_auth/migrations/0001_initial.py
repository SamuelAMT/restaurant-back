# Generated by Django 5.0.9 on 2024-11-14 03:53

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
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
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('custom_user_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('role', models.CharField(choices=[('SUPERADMIN', 'Super Admin'), ('RESTAURANT_ADMIN', 'Restaurant Admin'), ('RESTAURANT_SUB_ADMIN', 'Restaurant Sub Admin'), ('RESTAURANT_STAFF', 'Restaurant Staff')], default='RESTAURANT_STAFF', max_length=20)),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='customeruser_set', to='auth.group', verbose_name='groups')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
