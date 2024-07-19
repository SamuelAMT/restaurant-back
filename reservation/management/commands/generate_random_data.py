import random
from django.core.management.base import BaseCommand
from faker import Faker
from restaurant.models import Restaurant
from restaurant_customer.models import RestaurantCustomer
from reservation.models import Reservation, RestaurantVisit

class Command(BaseCommand):
    help = 'Generate random data for testing'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create fake restaurants
        for _ in range(5):
            restaurant = Restaurant.objects.create(
                cnpj=fake.ssn(),
                name=fake.company(),
                country_code=fake.country_code(),
                phone=fake.phone_number(),
                email=fake.email(),
                website=fake.url(),
                description=fake.text(),
                image=fake.image_url()
            )

            # Create fake customers and reservations
            for _ in range(10):
                customer = RestaurantCustomer.objects.create(
                    name=fake.first_name(),
                    lastname=fake.last_name(),
                    country_code=fake.country_code(),
                    phone=fake.phone_number(),
                    email=fake.email(),
                    birthdate=fake.date_of_birth()
                )

                visit = RestaurantVisit.objects.create(
                    restaurant=restaurant,
                    restaurant_customer=customer
                )

                for _ in range(random.randint(1, 5)):
                    Reservation.objects.create(
                        reserver=fake.name(),
                        amount_of_people=random.randint(1, 15),
                        amount_of_hours=random.randint(1, 5),
                        time=random.randint(0, 23),
                        date=fake.date_this_year(),
                        visit=visit
                    )

        self.stdout.write(self.style.SUCCESS('Successfully generated random data'))
