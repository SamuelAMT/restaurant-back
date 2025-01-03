import pytest
from ..services.restaurant_service import RestaurantService
from ..services.reservation_service import ReservationService
from datetime import datetime, time

@pytest.mark.django_db
class TestRestaurantService:
    def test_create_restaurant(self, admin_user, category):
        restaurant = RestaurantService.create_restaurant(
            name="Test Restaurant",
            cnpj="12345678901234",
            admin_user=admin_user,
            category_id=category.category_id,
            cuisine_type_ids=[]
        )
        assert restaurant.name == "Test Restaurant"
        assert restaurant.units.filter(is_main_unit=True).exists()

    def test_set_working_hours(self, restaurant_unit):
        working_hours = RestaurantService.set_working_hours(
            restaurant_unit.unit_id,
            [{
                "day_of_week": 0,
                "opening_time": time(9, 0),
                "closing_time": time(18, 0)
            }]
        )
        assert len(working_hours) == 1
        assert working_hours[0].opening_time == time(9, 0)

@pytest.mark.django_db
class TestReservationService:
    def test_create_reservation(self, restaurant, restaurant_unit):
        reservation = ReservationService.create_reservation(
            restaurant.restaurant_id,
            restaurant_unit.unit_id,
            {
                "reserver": "John Doe",
                "amount_of_people": 2,
                "start_time": time(12, 0),
                "end_time": time(14, 0),
                "reservation_date": datetime.now().date()
            }
        )
        assert reservation["reserver"] == "John Doe"
        assert reservation["amount_of_people"] == 2