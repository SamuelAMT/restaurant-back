# Generated by Django 5.0.6 on 2024-06-25 23:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_alter_address_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='id',
            new_name='address_id',
        ),
    ]
