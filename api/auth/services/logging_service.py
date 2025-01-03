from custom_auth.models import LoginLog
from typing import Any

class LoggingService:
    @staticmethod
    def log_auth_action(user: Any, request: Any, action: str) -> None:
        """Log authentication-related actions."""
        ip_address = request.META.get("REMOTE_ADDR", 
                                    request.META.get('HTTP_X_FORWARDED_FOR', ''))
        
        LoginLog.objects.create(
            custom_user=user,
            ip_address=ip_address,
            action=action
        )