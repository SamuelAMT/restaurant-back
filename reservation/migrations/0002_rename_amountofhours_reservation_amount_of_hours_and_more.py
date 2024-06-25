# Generated by Django 5.0.6 on 2024-06-25 23:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='amountOfHours',
            new_name='amount_of_hours',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='amountOfPeople',
            new_name='amount_of_people',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='email',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='name',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='phone',
        ),
    ]
