from typing import Any, Optional
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from ..schemas.auth import TokenSchema
from .logging_service import LoggingService


class AuthService:
    @staticmethod
    def authenticate_user(
            request: Any,
            email: str,
            password: str,
            superuser_required: bool = False,
            allowed_roles: Optional[list[str]] = None
    ) -> tuple[Any, TokenSchema | None]:
        """
        Authenticate a user and return tokens if successful.
        """
        user = authenticate(request, username=email, password=password)

        if user is None:
            return None, None

        if superuser_required and not user.is_superuser:
            return None, None

        if not superuser_required and user.is_superuser:
            return None, None

        user_role = getattr(user, 'role', None)
        if allowed_roles and user_role not in allowed_roles:
            return None, None

        refresh = RefreshToken.for_user(user)

        # Get the appropriate unit for logging based on user role
        user_unit = None
        if hasattr(user, 'unit'):
            user_unit = user.unit
        elif hasattr(user, 'restaurant') and user.role == 'RESTAURANT_ADMIN':
            user_unit = user.restaurant.units.filter(is_main_unit=True).first() or user.restaurant.units.first()

        LoggingService.log_auth_action(user, request, "login", user_unit)

        return user, TokenSchema(
            access=str(refresh.access_token),
            refresh=str(refresh),
            email=user.email,
            is_superuser=user.is_superuser,
            role=user_role
        )

    @staticmethod
    def get_restaurant_data(user: Any, restaurant: Any) -> dict | None:
        """
        Get formatted restaurant data for response based on user role.

        Args:
            user: The authenticated user
            restaurant: The associated restaurant
        """
        if not restaurant:
            return None

        base_data = {
            "restaurant_id": str(restaurant.restaurant_id),
            "cnpj": restaurant.cnpj,
            "name": restaurant.name,
            "country_code": restaurant.country_code,
            "phone": restaurant.phone,
            "email": restaurant.email,
            "email_verified": restaurant.email_verified,
            "image": restaurant.image.url if restaurant.image else None,
            "website": restaurant.website,
            "description": restaurant.description,
            "created_at": restaurant.created_at,
            "updated_at": restaurant.updated_at,
        }

        # RESTAURANT_ADMIN sees all units
        if user.role == 'RESTAURANT_ADMIN':
            units_data = []
            for unit in restaurant.units.all():
                units_data.append({
                    "unit_id": str(unit.unit_id),
                    "name": unit.name,
                    "is_main_unit": unit.is_main_unit,
                    "created_at": unit.created_at,
                    "updated_at": unit.updated_at,
                })
            base_data["units"] = units_data
            base_data["customers"] = [
                str(customer.restaurant_customer_id)
                for customer in restaurant.customers.all()
            ]
        # Other roles only see their assigned unit
        elif hasattr(user, 'unit'):
            unit = user.unit
            base_data["unit"] = {
                "unit_id": str(unit.unit_id),
                "name": unit.name,
                "is_main_unit": unit.is_main_unit,
                "created_at": unit.created_at,
                "updated_at": unit.updated_at,
            }

        return base_data