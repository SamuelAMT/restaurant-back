from typing import Any
from ninja import Router
from ..services.auth_service import AuthService
from ..schemas.auth import LoginSchema
from ..schemas.responses import ErrorSchema
from .base import BaseAuthRouter

admin_auth_router = BaseAuthRouter()

@admin_auth_router.post("/login/", response={200: dict, 401: ErrorSchema})
def admin_login(request, payload: LoginSchema):
    """API endpoint for superuser authentication."""
    user, token_data = AuthService.authenticate_user(
        request, payload.email, payload.password, superuser_required=True
    )
    
    if user and token_data:
        return token_data.dict()
    return 401, {"detail": "Invalid credentials or insufficient permissions"}