from typing import Any
from custom_auth.authentication import JWTAuth
from ..services.auth_service import AuthService
from ..schemas.auth import LoginSchema, TokenSchema
from ..schemas.responses import ErrorSchema, MessageSchema
from .base import BaseAuthRouter

user_auth_router = BaseAuthRouter()

@user_auth_router.post("/login/", response={200: dict, 401: ErrorSchema})
def user_login(request, payload: LoginSchema):
    """API endpoint for regular user authentication."""
    user, token_data = AuthService.authenticate_user(
        request, payload.email, payload.password
    )
    
    if user and token_data:
        response_data = token_data.dict()
        restaurant_data = AuthService.get_restaurant_data(
            getattr(user, 'restaurant', None)
        )
        if restaurant_data:
            response_data["restaurant"] = restaurant_data
        return response_data
    return 401, {"detail": "Invalid credentials"}

@user_auth_router.post("/token/refresh/", response={200: TokenSchema, 401: ErrorSchema})
def token_refresh(request, payload: dict):
    token_data, error = BaseAuthRouter.refresh_token(payload.get("refresh"))
    if token_data:
        return token_data.dict()
    return 401, {"detail": error or "Invalid refresh token"}

@user_auth_router.post("/logout/", auth=JWTAuth(), response=MessageSchema)
def logout(request):
    return BaseAuthRouter.logout_user(request)