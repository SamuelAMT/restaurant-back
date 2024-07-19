from ninja import NinjaAPI
from restaurant_customer.models import RestaurantCustomer

api = NinjaAPI(urls_namespace='backend-restaurant-api')

@api.get("/customer-reservations/", response=list)
def customer_reservations(request):
    customers = RestaurantCustomer.objects.all().select_related('reservations')
    result = []
    for customer in customers:
        for reservation in customer.reservations.all():
            result.append({
                'customer_name': f"{customer.name} {customer.lastname}",
                'email': customer.email,
                'phone': customer.phone,
                'amount_of_people': reservation.amount_of_people,
                'amount_of_hours': reservation.amount_of_hours
            })
    return result
