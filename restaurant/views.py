from django.shortcuts import render
from django.http import HttpRequest

def dashboard_view(request: HttpRequest, restaurant_name: str):
    return render(request, 'restaurant/dashboard.html', {'restaurant_name': restaurant_name})

def reservations_view(request: HttpRequest, restaurant_name: str):
    return render(request, 'restaurant/reservations.html', {'restaurant_name': restaurant_name})

def customers_view(request: HttpRequest, restaurant_name: str):
    return render(request, 'restaurant/customers.html', {'restaurant_name': restaurant_name})

def settings_view(request: HttpRequest, restaurant_name: str):
    return render(request, 'restaurant/settings.html', {'restaurant_name': restaurant_name})
