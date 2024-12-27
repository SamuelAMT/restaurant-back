# Generated by Django 5.0.9 on 2024-12-27 00:36

import django.utils.timezone
import reservation.models
from django.db import migrations, models
import uuid

class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0014_alter_reservation_table'),
        ('restaurant', '0007_restaurantemployee_country_code'),
        ('restaurant_customer', '0005_remove_restaurantcustomer_restaurant__name_78fb79_idx_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='reservation',
            name='reservation_reservation_reservation_hash_150a83e3_like',
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reservation_hash',
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                db_index=True,
            ),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='amount_of_hours',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='amount_of_people',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reservation_date',
            field=models.DateField(db_index=True),
        ),
        migrations.AddConstraint(
            model_name='reservation',
            constraint=models.CheckConstraint(check=models.Q(amount_of_people__gt=0), name='positive_people_amount'),
        ),
    ]