from ninja import Router
from django.http import HttpRequest
from typing import List
from datetime import datetime
from django.shortcuts import get_object_or_404
from ...services.restaurant_service import RestaurantService
from ..schemas.restaurant import (
    RestaurantCreateSchema,
    RestaurantResponseSchema,
)
from ...models.restaurant import Restaurant

restaurant_router = Router()


@restaurant_router.get("/", response=List[RestaurantResponseSchema])
def list_restaurants(request: HttpRequest):
    restaurants = RestaurantService.get_restaurants()
    return [_format_restaurant_response(restaurant) for restaurant in restaurants]


def _format_restaurant_response(restaurant: Restaurant) -> RestaurantResponseSchema:
    return RestaurantResponseSchema(
        restaurant_id=restaurant.restaurant_id,
        name=restaurant.name,
        cnpj=restaurant.cnpj,
        category=restaurant.category.name if restaurant.category else None,
        cuisine_types=[ct.name for ct in restaurant.cuisine_types.all()],
        country_code=restaurant.country_code,
        phone=restaurant.phone,
        email=restaurant.email,
        website=restaurant.website,
        description=restaurant.description,
        image=restaurant.image,
        role=restaurant.role,
        addresses=[
            {
                "id": str(addr.address_id),
                "cep": addr.cep,
                "street": addr.street,
                "number": addr.number,
                "neighborhood": addr.neighborhood,
                "city": addr.city,
                "state": addr.state,
                "country": addr.country,
                "complement": addr.complement,
                "maps_url": addr.maps_url,
            }
            for addr in restaurant.addresses.all()
        ],
        units=[
            {
                "unit_id": unit.unit_id,
                "name": unit.name,
                "is_main_unit": unit.is_main_unit,
                "working_hours": [...],
                "blocked_hours": [...],
            }
            for unit in restaurant.units.all()
        ],
    )


@restaurant_router.post("/", response=RestaurantResponseSchema)
def create_restaurant(request: HttpRequest, payload: RestaurantCreateSchema):
    restaurant = RestaurantService.create_restaurant(
        name=payload.name,
        cnpj=payload.cnpj,
        admin_user=request.user,
        category_id=payload.category_id,
        cuisine_type_ids=payload.cuisine_type_ids,
        country_code=payload.country_code,
        phone=payload.phone,
        email=payload.email,
        website=payload.website,
        description=payload.description,
        image=payload.image,
    )
    return _format_restaurant_response(restaurant)
