# Generated by Django 5.0.9 on 2025-01-06 14:39

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('unit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('address_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cep', models.CharField(max_length=9, validators=[django.core.validators.RegexValidator(message='CEP must be in the format 00000-000', regex='^\\d{5}-?\\d{3}$')])),
                ('street', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=10)),
                ('neighborhood', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=2)),
                ('country', models.CharField(max_length=50)),
                ('complement', models.CharField(blank=True, max_length=100)),
                ('maps_url', models.URLField(blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('unit', models.OneToOneField(db_column='unit_id', on_delete=django.db.models.deletion.CASCADE, related_name='address', to='unit.unit')),
            ],
            options={
                'indexes': [models.Index(fields=['city', 'state'], name='address_city_state_idx')],
                'unique_together': {('cep', 'street', 'number', 'neighborhood', 'city', 'state', 'country')},
            },
        ),
    ]
