from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'restaurant/index.html')

def dashboard(request):
    return render(request, 'restaurant/dashboard.html')

def calendar(request):
    return render(request, 'restaurant/calendar.html')

def customer_list(request):
    return render(request, 'restaurant/customer-list.html')

def settings(request):
    return render(request, 'restaurant/settings.html')