from ninja import Router
from pydantic import BaseModel

router = Router()

class ReservationSchema(BaseModel):
    restaurant_id: int
    customer_name: str
    reservation_time: str

@router.get("/")
def list_reservations(request):
    # Your logic to list reservations
    return {"reservations": []}

@router.post("/")
def create_reservation(request, reservation: ReservationSchema):
    # Your logic to create a reservation
    return {"message": "Reservation created", "reservation": reservation}
