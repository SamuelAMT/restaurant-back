import pytest
from django.core.exceptions import ValidationError
from ..models import Restaurant, RestaurantUnit, WorkingHours, BlockedHours
from datetime import datetime, time

@pytest.mark.django_db
class TestRestaurant:
    def test_create_restaurant(self, admin_user):
        restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            cnpj="12345678901234",
            admin=admin_user
        )
        assert restaurant.name == "Test Restaurant"
        assert restaurant.cnpj == "12345678901234"
        
    def test_create_unit(self, restaurant):
        unit = RestaurantUnit.objects.create(
            restaurant=restaurant,
            name="Main Unit",
            is_main_unit=True
        )
        assert unit.name == "Main Unit"
        assert unit.is_main_unit is True

    def test_working_hours(self, restaurant_unit):
        working_hours = WorkingHours.objects.create(
            unit=restaurant_unit,
            day_of_week=0,  # Monday
            opening_time=time(9, 0),
            closing_time=time(18, 0)
        )
        assert working_hours.day_of_week == 0
        assert working_hours.opening_time == time(9, 0)
        
    def test_blocked_hours(self, restaurant_unit):
        blocked_hours = BlockedHours.objects.create(
            unit=restaurant_unit,
            start_datetime=datetime(2024, 12, 25, 0, 0),
            end_datetime=datetime(2024, 12, 26, 0, 0),
            reason="Christmas"
        )
        assert blocked_hours.reason == "Christmas"