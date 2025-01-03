from ninja import Router
from django.http import HttpRequest
from ..schemas.settings import SettingsSchema, SettingsUpdateSchema

settings_router = Router()

@settings_router.get("/{restaurant_id}/settings", response=SettingsSchema)
def get_settings(request: HttpRequest, restaurant_id: str):
    return {
        "theme": "dark",
        "currency": "BRL",
        "notification_enabled": True
    }

@settings_router.patch("/{restaurant_id}/settings")
def update_settings(request: HttpRequest, restaurant_id: str, payload: SettingsUpdateSchema):
    # Implement settings update logic
    return {"status": "success"}