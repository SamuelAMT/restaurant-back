from ninja import Router
from .prisma_client import prisma

router = Router()

@router.get("/items")
def get_items(request):
    items = prisma.item.find_many()
    return items