# restaurant/api.py

from ninja import Router, Schema
from typing import List
from pydantic import EmailStr, AnyUrl
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from typing import Optional
from address.models import Address
from restaurant.models import Restaurant
from reservation.models import Reservation
from restaurant_customer.models import RestaurantCustomer

restaurant_router = Router()

class AddressSchema(Schema):
    cep: str
    street: str
    number: str
    neighborhood: str
    city: str
    state: str
    country: str
    complement: str = None

class RestaurantCreateSchema(Schema):
    cnpj: str
    name: str
    country_code: str
    phone: str
    email: EmailStr
    email_verified: EmailStr
    image: AnyUrl
    website: AnyUrl
    description: str
    role: str
    admin: int
    customers: List[int]
    employees: List[int]
    login_logs: List[int]
    addresses: List[AddressSchema]

class RestaurantSchema(Schema):
    restaurant_id: str
    cnpj: str
    name: str
    country_code: str
    phone: str
    email: EmailStr
    email_verified: EmailStr
    image: AnyUrl

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
    birthday: Optional[str] = None
    observation: Optional[str] = None

class CustomerSchema(Schema):
    name: str
    lastname: str
    phone: str
    email: str
    birthday: Optional[str] = None

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

@restaurant_router.post("/", response=RestaurantSchema)
def create_restaurant(request: HttpRequest, payload: RestaurantCreateSchema):
    restaurant = Restaurant.objects.create(
        cnpj=payload.cnpj,
        name=payload.name,
        country_code=payload.country_code,
        phone=payload.phone,
        email=payload.email,
        email_verified=payload.email_verified,
        image=payload.image,
        website=payload.website,
        description=payload.description,
        role=payload.role,
        admin_id=payload.admin,
    )

    restaurant.customers.set(payload.customers)
    restaurant.employees.set(payload.employees)
    restaurant.login_logs.set(payload.login_logs)

    for addr in payload.addresses:
        Address.objects.create(
            restaurant=restaurant,
            cep=addr.cep,
            street=addr.street,
            number=addr.number,
            neighborhood=addr.neighborhood,
            city=addr.city,
            state=addr.state,
            country=addr.country,
            complement=addr.complement,
        )

    return RestaurantSchema(
        restaurant_id=str(restaurant.restaurant_id),
        cnpj=restaurant.cnpj,
        name=restaurant.name,
        country_code=restaurant.country_code,
        phone=restaurant.phone,
        email=restaurant.email,
        email_verified=restaurant.email_verified,
        image=restaurant.image,
    )

@restaurant_router.get("/{restaurant_id}/dashboard", response=DashboardSchema)
def get_dashboard(request: HttpRequest, restaurant_id: str):
    restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
    total_reservations = restaurant.reservation_set.count()
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

@restaurant_router.get("/{restaurant_id}/reservations", response=list[ReservationSchema])
def list_reservations(request: HttpRequest, restaurant_id: str):
    restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
    reservations = Reservation.objects.filter(visit__restaurant=restaurant)
    return [
        ReservationSchema(
            reserver=res.reserver,
            amount_of_people=res.amount_of_people,
            amount_of_hours=res.amount_of_hours,
            time=res.time,
            date=str(res.date),
            email=res.email,
            phone=res.phone,
            birthday=str(res.birthday) if res.birthday else None,
            observation=res.observation,
        )
        for res in reservations
    ]

@restaurant_router.post("/{restaurant_id}/reservations", response=ReservationSchema)
def create_reservation(request: HttpRequest, restaurant_id: str, payload: ReservationSchema):
    restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
    reservation = Reservation.objects.create(
        reserver=payload.reserver,
        amount_of_people=payload.amount_of_people,
        amount_of_hours=payload.amount_of_hours,
        time=payload.time,
        date=payload.date,
        email=payload.email,
        phone=payload.phone,
        birthday=payload.birthday,
        observation=payload.observation,
        visit=restaurant.restaurantvisit_set.first(),
    )
    return reservation

@restaurant_router.get("/{restaurant_id}/customers", response=list[CustomerSchema])
def list_customers(request: HttpRequest, restaurant_id: str):
    restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
    customers = restaurant.customers.all()
    return [
        CustomerSchema(
            name=customer.name,
            lastname=customer.lastname,
            phone=customer.phone,
            email=customer.email,
            birthday=str(customer.birthday) if customer.birthday else None,
        )
        for customer in customers
    ]

@restaurant_router.post("/{restaurant_id}/customers", response=CustomerSchema)
def create_customer(request: HttpRequest, restaurant_id: str, payload: CustomerSchema):
    restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
    customer = RestaurantCustomer.objects.create(
        name=payload.name,
        lastname=payload.lastname,
        email=payload.email,
        phone=payload.phone,
        birthday=payload.birthday,
    )
    restaurant.customers.add(customer)
    return customer

@restaurant_router.get("/{restaurant_id}/settings", response=list[SettingsSchema])
def get_settings(request: HttpRequest, restaurant_id: str):
    settings = [
        SettingsSchema(setting_key="theme", setting_value="dark"),
        SettingsSchema(setting_key="currency", setting_value="BRL"),
    ]
    return settings

@restaurant_router.get("/{restaurant_id}/profile", response=ProfileSchema)
def get_profile(request: HttpRequest, restaurant_id: str):
    restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
    address = restaurant.addresses.first() if restaurant.addresses.exists() else None
    return ProfileSchema(
        name=restaurant.name,
        email=restaurant.email or "",
        phone=restaurant.phone or "",
        website=restaurant.website or "",
        description=restaurant.description or "",
        address=(
            f"{address.street}, {address.number} - {address.neighborhood}"
            if address else "No address"
        ),
    )