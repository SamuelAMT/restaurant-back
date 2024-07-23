from ninja import Router, Schema

router = Router()

# Define the schema for requests and responses
class RestaurantSchema(Schema):
    name: str
    address: str

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
@router.get("/dashboard", response=DashboardSchema)
def get_dashboard(request):
    # Your logic to fetch dashboard data
    return DashboardSchema(total_reservations=100, total_customers=50)

@router.get("/reserves", response=ReservationSchema)
def list_reservations(request):
    # Your logic to list reservations
    return [ReservationSchema(reserver="John Doe", time="12:00", date="2024-07-10")]

@router.get("/customers", response=CustomerSchema)
def list_customers(request):
    # Your logic to list customers
    return [CustomerSchema(name="John Doe", email="john@example.com")]

@router.get("/settings", response=SettingsSchema)
def get_settings(request):
    # Your logic to fetch settings
    return [SettingsSchema(setting_key="theme", setting_value="dark")]

@router.get("/profile", response=ProfileSchema)
def get_profile(request):
    # Your logic to fetch profile
    return ProfileSchema(username="john_doe", email="john@example.com")
