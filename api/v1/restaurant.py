from ninja import Router, Schema
from django.http import HttpRequest
from address.models import Address
from restaurant.models import Restaurant
from reservation.models import Reservation
from restaurant_customer.models import RestaurantCustomer

router = Router()


class DashboardSchema(Schema):
    total_reservations: int
    new_customers: int
    new_reservations: int
    total_customers: int
    canceled_reservations: int


class ReservationSchema(Schema):
    reserver: str
    amount_of_people: int
    amount_of_hours: int
    time: int
    date: str
    email: str
    phone: str


class CustomerSchema(Schema):
    name: str
    lastname: str
    phone: str
    email: str


class SettingsSchema(Schema):
    setting_key: str
    setting_value: str


class ProfileSchema(Schema):
    name: str
    email: str
    phone: str
    website: str
    description: str
    address: str


@router.get("/{restaurant_name}/dashboard", response=DashboardSchema)
def get_dashboard(request: HttpRequest, restaurant_name: str):
    try:
        restaurant = Restaurant.objects.get(name=restaurant_name)
        total_reservations = restaurant.restaurant_visits.count()
        total_customers = restaurant.customers.count()
        canceled_reservations = 0
        new_customers = 0
        new_reservations = 0

        return DashboardSchema(
            total_reservations=total_reservations,
            new_customers=new_customers,
            new_reservations=new_reservations,
            total_customers=total_customers,
            canceled_reservations=canceled_reservations,
        )
    except Restaurant.DoesNotExist:
        return {"error": "Restaurant not found"}, 404


@router.get("/{restaurant_name}/reservations", response=list[ReservationSchema])
def list_reservations(request: HttpRequest, restaurant_name: str):
    try:
        restaurant = Restaurant.objects.get(name=restaurant_name)
        reservations = Reservation.objects.filter(visit__restaurant=restaurant)
        return [
            ReservationSchema(
                reserver=res.reserver,
                amount_of_people=res.amount_of_people,
                amount_of_hours=res.amount_of_hours,
                time=res.time,
                date=res.date,
                email="example@example.com",
                phone="123456789",
            )
            for res in reservations
        ]
    except Restaurant.DoesNotExist:
        return {"error": "Restaurant not found"}, 404


@router.get("/{restaurant_name}/customers", response=list[CustomerSchema])
def list_customers(request: HttpRequest, restaurant_name: str):
    try:
        restaurant = Restaurant.objects.get(name=restaurant_name)
        customers = restaurant.customers.all()
        return [
            CustomerSchema(
                name=customer.name,
                lastname=customer.lastname,
                phone=customer.phone,
                email=customer.email or "",
            )
            for customer in customers
        ]
    except Restaurant.DoesNotExist:
        return {"error": "Restaurant not found"}, 404


@router.get("/{restaurant_name}/settings", response=list[SettingsSchema])
def get_settings(request: HttpRequest, restaurant_name: str):
    settings = [
        SettingsSchema(setting_key="theme", setting_value="dark"),
        SettingsSchema(setting_key="currency", setting_value="BRL"),
    ]
    return settings


@router.get("/profile", response=ProfileSchema)
def get_profile(request: HttpRequest):
    try:
        restaurant = Restaurant.objects.first()
        address = (
            restaurant.addresses.first() if restaurant.addresses.exists() else None
        )
        return ProfileSchema(
            name=restaurant.name,
            email=restaurant.email or "",
            phone=restaurant.phone or "",
            website=restaurant.website or "",
            description=restaurant.description or "",
            address=f"{address.street}, {address.number} - {address.neighborhood}"
            if address
            else "No address",
        )
    except Restaurant.DoesNotExist:
        return {"error": "Restaurant not found"}, 404
