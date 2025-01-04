# Generated by Django 5.0.9 on 2025-01-04 21:01

from django.db import migrations
import uuid

def convert_ids_to_uuid(apps, schema_editor):
    Address = apps.get_model('address', 'Address')
    for address in Address.objects.all():
        if isinstance(address.address_id, (int, str)) and not isinstance(address.address_id, uuid.UUID):
            address.address_id = uuid.uuid4()
            address.save()

def reverse_convert(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('address', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(convert_ids_to_uuid, reverse_convert),
    ]