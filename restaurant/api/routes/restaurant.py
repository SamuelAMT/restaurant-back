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
from unit.api.routes.unit import _format_unit_response

restaurant_router = Router()


@restaurant_router.get("/", response=List[RestaurantResponseSchema])
def list_restaurants(request: HttpRequest):
    restaurants = RestaurantService.get_restaurants()
    return [_format_restaurant_response(restaurant) for restaurant in restaurants]


def _format_restaurant_response(restaurant: Restaurant) -> RestaurantResponseSchema:
    units = restaurant.units.all()
    addresses = []
    for unit in units:
        if unit.address:
            addresses.append({
            "address_id": unit.address.address_id,
            "cep": unit.address.cep,
            "street": unit.address.street,
            "number": unit.address.number,
            "neighborhood": unit.address.neighborhood,
            "city": unit.address.city,
            "state": unit.address.state,
            "country": unit.address.country,
            "complement": unit.address.complement or None,
            "maps_url": unit.address.maps_url if unit.address.maps_url else None
            })

    image_url = str(restaurant.image.url) if restaurant.image else None

    return RestaurantResponseSchema(
        restaurant_id=restaurant.restaurant_id,
        name=restaurant.name,
        cnpj=restaurant.cnpj,
        category=restaurant.category.name if restaurant.category else None,
        cuisine_types=[ct.name for ct in restaurant.cuisine_types.all()],
        country_code=restaurant.country_code,
        phone=restaurant.phone,
        email=restaurant.email,
        website=str(restaurant.website) if restaurant.website else None,
        description=restaurant.description,
        image=image_url,
        role=restaurant.role,
        addresses=addresses,
        units=[_format_unit_response(unit) for unit in units],
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
