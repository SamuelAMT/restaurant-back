
from django.db import migrations
from django.core.exceptions import ObjectDoesNotExist

def assign_units_to_employees(apps, schema_editor):
    RestaurantEmployee = apps.get_model('restaurant', 'RestaurantEmployee')
    RestaurantUnit = apps.get_model('restaurant', 'RestaurantUnit')
    Restaurant = apps.get_model('restaurant', 'Restaurant')

    for employee in RestaurantEmployee.objects.filter(unit__isnull=True):
        try:
            # Find the restaurant(s) this employee belongs to
            restaurants = employee.restaurants.all()
            
            if not restaurants:
                print(f"Warning: Employee {employee.email} is not associated with any restaurant")
                continue
                
            # Use the first restaurant's main unit
            restaurant = restaurants.first()
            main_unit = RestaurantUnit.objects.filter(
                restaurant=restaurant,
                is_main_unit=True
            ).first()
            
            if main_unit:
                employee.unit = main_unit
                employee.save()
            else:
                # If no main unit exists, create one
                main_unit = RestaurantUnit.objects.create(
                    restaurant=restaurant,
                    name=f"{restaurant.name} - Main Unit",
                    is_main_unit=True
                )
                employee.unit = main_unit
                employee.save()
                print(f"Created main unit for restaurant {restaurant.name} and assigned employee {employee.email}")
                
        except Exception as e:
            print(f"Error processing employee {employee.email}: {str(e)}")

def reverse_func(apps, schema_editor):
    """
    In case we need to reverse this migration, we'll set all unit fields to null
    """
    RestaurantEmployee = apps.get_model('restaurant', 'RestaurantEmployee')
    RestaurantEmployee.objects.all().update(unit=None)

class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0008_blockedhours_cuisinetype_restaurantcategory_and_more'),
    ]

    operations = [
        migrations.RunPython(assign_units_to_employees, reverse_func),
    ]