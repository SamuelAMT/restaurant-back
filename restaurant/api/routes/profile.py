from ninja import Router
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ...services.profile_service import ProfileService
from ..schemas.profile import ProfileSchema

profile_router = Router()

@profile_router.get("/{restaurant_id}/profile", response=ProfileSchema)
def get_profile(request: HttpRequest, restaurant_id: str):
    return ProfileService.get_profile(restaurant_id)