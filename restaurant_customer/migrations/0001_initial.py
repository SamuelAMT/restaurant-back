import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    operations = [
        migrations.CreateModel(
            name='RestaurantCustomer',
            fields=[
                ('restaurant_customer_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=70, unique=True)),
                ('country_code', models.CharField(blank=True, max_length=3, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('units', models.ManyToManyField(blank=True, related_name='unit_customers', to='unit.unit')),
            ],
            options={
                'db_table': 'restaurant_customer',
                'indexes': [models.Index(fields=['first_name', 'last_name', 'phone'], name='restaurant__name_78fb79_idx')],
            },
        ),
    ]