import pytest
from ninja.testing import TestClient
from ..api.routes.restaurant import restaurant_router
from ..api.routes.reservation import reservation_router

@pytest.mark.django_db
class TestRestaurantAPI:
    def setup_method(self):
        self.client = TestClient(restaurant_router)

    def test_create_restaurant(self, admin_user):
        response = self.client.post(
            "/",
            json={
                "name": "Test Restaurant",
                "cnpj": "12345678901234",
                "category_id": "valid-uuid",
                "cuisine_type_ids": []
            }
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Test Restaurant"

@pytest.mark.django_db
class TestReservationAPI:
    def setup_method(self):
        self.client = TestClient(reservation_router)

    def test_create_reservation(self, restaurant):
        response = self.client.post(
            f"/{restaurant.restaurant_id}/reservations",
            json={
                "reserver": "John Doe",
                "amount_of_people": 2,
                "start_time": "12:00",
                "end_time": "14:00",
                "reservation_date": "2024-12-27"
            }
        )
        assert response.status_code == 200
        assert response.json()["reserver"] == "John Doe"