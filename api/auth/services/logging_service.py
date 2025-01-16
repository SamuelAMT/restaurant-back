from custom_auth.models import LoginLog
from typing import Any, Optional
from unit.models import Unit


class LoggingService:
    @staticmethod
    def log_auth_action(user: Any, request: Any, action: str, unit: Optional[Unit] = None) -> None:
        """
        Log authentication-related actions.

        Args:
            user: The user performing the action
            request: The HTTP request
            action: The action being performed (e.g., 'login', 'logout')
            unit: The unit associated with the action (optional)
        """
        ip_address = request.META.get("REMOTE_ADDR",
                                      request.META.get('HTTP_X_FORWARDED_FOR', ''))
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')

        if not unit and hasattr(user, 'restaurant'):
            unit = user.restaurant.units.filter(is_main_unit=True).first()
            if not unit:
                unit = user.restaurant.units.first()

        if unit:
            LoginLog.objects.create(
                custom_user=user,
                unit=unit,
                ip_address=ip_address,
                user_agent=user_agent,
                action=action
            )