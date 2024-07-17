from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.http import Http404

# Create your views here.
# Integrate frontend with backend
def index(request):
    return render(request, 'restaurant/index.html')

def login(request):
    return render(request, 'restaurant/login.html')

def dashboard(request):
    return render(request, 'restaurant/dashboard.html')

def calendar(request):
    return render(request, 'restaurant/calendar.html')

def customer_list(request):
    return render(request, 'restaurant/customer-list.html')

def settings(request):
    return render(request, 'restaurant/settings.html')