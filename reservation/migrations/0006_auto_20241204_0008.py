# Generated by Django 5.0.9 on 2024-12-04 03:08

from django.db import migrations
import uuid

def associate_reservations(apps, schema_editor):
    Reservation = apps.get_model('reservation', 'Reservation')
    RestaurantVisit = apps.get_model('reservation', 'RestaurantVisit')
    Restaurant = apps.get_model('restaurant', 'Restaurant')

    for reservation in Reservation.objects.filter(visit__isnull=True):
        default_restaurant, created = Restaurant.objects.get_or_create(
            name='Default Restaurant',
            defaults={
                'restaurant_id': uuid.uuid4(),
                'cnpj': '00000000000000',
                'country_code': 'XX',
                'phone': '0000000000',
                'email': 'default@example.com',
                'role': 'RESTAURANT_ADMIN',
                'admin_id': 1,
            }
        )

        visit, created = RestaurantVisit.objects.get_or_create(
            restaurant=default_restaurant
        )

        reservation.visit = visit
        reservation.save()

class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0005_alter_reservation_visit'),
    ]

    operations = [
        migrations.RunPython(associate_reservations),
    ]