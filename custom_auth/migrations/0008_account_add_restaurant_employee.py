# custom_auth/migrations/0008_account_add_restaurant_employee.py
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0007_alter_account_employee_alter_account_restaurant'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='restaurant',
            field=models.ForeignKey(
                related_name='auth_accounts',
                to='restaurant.Restaurant',
                on_delete=django.db.models.deletion.CASCADE,
                null=True,
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name='account',
            name='employee',
            field=models.ForeignKey(
                related_name='staff_accounts',
                to='restaurant.RestaurantEmployee',
                on_delete=django.db.models.deletion.CASCADE,
                null=True,
                blank=True,
            ),
        ),
    ]