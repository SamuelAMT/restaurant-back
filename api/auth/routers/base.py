from typing import Any
from ninja import Router
from rest_framework_simplejwt.tokens import RefreshToken
from custom_auth.authentication import JWTAuth
from ..schemas.auth import TokenSchema
from ..schemas.responses import ErrorSchema, MessageSchema
from ..services.logging_service import LoggingService

class BaseAuthRouter(Router):
    @staticmethod
    def refresh_token(refresh_token: str) -> tuple[TokenSchema | None, str | None]:
        """Refresh an authentication token."""
        try:
            refresh = RefreshToken(refresh_token)
            return TokenSchema(
                access=str(refresh.access_token),
                refresh=str(refresh)
            ), None
        except Exception:
            return None, "Invalid refresh token"
    
    @staticmethod
    def logout_user(request: Any) -> MessageSchema:
        """Log out a user by blacklisting their refresh token."""
        try:
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                refresh_token = auth_header.split()[1]
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            LoggingService.log_auth_action(request.user, request, "logout")
        except Exception:
            pass
        
        return MessageSchema(message="Logged out successfully")