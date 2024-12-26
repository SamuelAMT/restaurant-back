# Generated by Django 5.0.9 on 2024-12-04 04:05

from django.db import migrations

def populate_restaurant(apps, schema_editor):
    Reservation = apps.get_model('reservation', 'Reservation')
    Restaurant = apps.get_model('restaurant', 'Restaurant')
    default_restaurant = Restaurant.objects.first()
    if not default_restaurant:
        raise Exception("No default restaurant found. Please create a restaurant first.")

    reservations = Reservation.objects.filter(restaurant__isnull=True)
    reservations.update(restaurant=default_restaurant)

class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0008_remove_reservation_visit_reservation_country_code_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_restaurant),
    ]