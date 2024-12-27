# restaurant/migrations/000X_populate_unit_field.py

from django.db import migrations
from django.core.exceptions import ObjectDoesNotExist

def assign_units_to_employees(apps, schema_editor):
    RestaurantEmployee = apps.get_model('restaurant', 'RestaurantEmployee')
    RestaurantUnit = apps.get_model('restaurant', 'RestaurantUnit')
    Restaurant = apps.get_model('restaurant', 'Restaurant')  # Assuming such a model exists

    for employee in RestaurantEmployee.objects.filter(unit__isnull=True):
        try:
            # Logic to find the appropriate RestaurantUnit for the employee
            # Example: Assign to the main unit of the restaurant owned by the admin_user

            # Assuming RestaurantEmployee has a link to admin_user or another field to find the Restaurant
            # Since RestaurantEmployee does not have such a field in the provided context,
            # This example will assign to the first main unit found

            main_unit = RestaurantUnit.objects.filter(is_main_unit=True).first()
            if main_unit:
                employee.unit = main_unit
                employee.save()
            else:
                # If no main unit exists, optionally create one or handle accordingly
                raise ObjectDoesNotExist("No main unit available to assign to employees.")
        except ObjectDoesNotExist as e:
            # Handle the case where no main unit is found
            # For example, log the error or assign to a default unit
            # Here, we'll skip assigning to avoid breaking the migration
            print(f"Cannot assign unit for employee {employee.email}: {e}")

class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0008_blockedhours_cuisinetype_restaurantcategory_and_more'),  # Replace with your actual migration name
    ]

    operations = [
        migrations.RunPython(assign_units_to_employees),
    ]