# Generated by Django 5.0.9 on 2024-12-30 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0006_alter_address_options_alter_address_address_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='maps_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
