from ninja import Router, Schema
from django.http import HttpRequest

router = Router()

# Define the schema for requests and responses

class DashboardSchema(Schema):
    total_reservations: int
    new_customers: int
    new_reservations: int    
    total_customers: int
    canceled_reservations: int

class ReservationSchema(Schema):
    # Restaurant Customers in a specific day
    reserver: str
    amount_of_people: int
    amount_of_hours: str
    time: str
    """date: str""" # We already have the calendar
    email: str
    phone: str

class CustomerSchema(Schema):
    # The difference between this schema from the above is that this one is for the all time restaurant customers
    reserver: str
    amount_of_people: int
    amount_of_hours: str
    time: str
    """date: str""" # We already have the calendar
    email: str
    phone: str

class SettingsSchema(Schema):
    setting_key: str
    setting_value: str

class ProfileSchema(Schema):
    username: str
    email: str

# Define endpoints
@router.get("/{restaurant_name}/dashboard", response=DashboardSchema)
def get_dashboard(request, restaurant_name: str):
    # Your logic to fetch dashboard data for the specific restaurant
    return DashboardSchema(total_reservations=100, total_customers=50)

@router.get("/{restaurant_name}/reservations", response=ReservationSchema)
def list_reservations(request, restaurant_name: str):
    # Your logic to list reservations for the specific restaurant
    return [ReservationSchema(reserver="John Doe", amount_of_people=4, amount_of_hours="2", time="12:00", email="john@example.com", phone="123456789")]

@router.get("/{restaurant_name}/customers", response=CustomerSchema)
def list_customers(request, restaurant_name: str):
    # Your logic to list customers for the specific restaurant
    return [CustomerSchema(reserver="John Doe", amount_of_people=4, amount_of_hours="2", time="12:00", email="john@example.com", phone="123456789")]

@router.get("/{restaurant_name}/settings", response=SettingsSchema)
def get_settings(request, restaurant_name: str):
    # Your logic to fetch settings for the specific restaurant
    return [SettingsSchema(setting_key="theme", setting_value="dark")]

@router.get("/profile", response=ProfileSchema)
def get_profile(request):
    # Your logic to fetch profile
    return ProfileSchema(username="john_doe", email="john@example.com")
