# Generated by Django 5.0.6 on 2024-07-19 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('restaurant_customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('cnpj', models.CharField(db_index=True, max_length=14, primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('country_code', models.CharField(max_length=3)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(blank=True, max_length=70, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.URLField(blank=True, null=True)),
                ('customers', models.ManyToManyField(related_name='restaurants', to='restaurant_customer.restaurantcustomer')),
            ],
            options={
                'indexes': [models.Index(fields=['cnpj', 'name'], name='restaurant__cnpj_8b2fef_idx')],
            },
        ),
    ]