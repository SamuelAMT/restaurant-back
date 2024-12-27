from ninja import Schema

class DashboardSchema(Schema):
    total_reservations: int
    new_customers: int
    new_reservations: int
    total_customers: int
    canceled_reservations: int