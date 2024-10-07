from ninja import Router

reservation_router = Router()

@reservation_router.get("/")
def get_reservations(request):
    return {"reservations": "list of reservations"}
