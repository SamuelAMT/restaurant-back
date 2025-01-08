from typing import Any
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from ..schemas.auth import TokenSchema
from .logging_service import LoggingService

class AuthService:
    @staticmethod
    def authenticate_user(request: Any, email: str, password: str, 
                         superuser_required: bool = False) -> tuple[Any, TokenSchema | None]:
        """Authenticate a user and return tokens if successful."""
        user = authenticate(request, username=email, password=password)
        
        if user is None:
            return None, None
            
        if superuser_required and not user.is_superuser:
            return None, None
        
        if not superuser_required and user.is_superuser:
            return None, None
            
        refresh = RefreshToken.for_user(user)
        LoggingService.log_auth_action(user, request, "login")
        
        return user, TokenSchema(
            access=str(refresh.access_token),
            refresh=str(refresh),
            email=user.email,
            is_superuser=user.is_superuser,
            role=getattr(user, 'role', None)
        )
    
    @staticmethod
    def get_restaurant_data(restaurant) -> dict | None:
        """Get formatted restaurant data for response."""
        if not restaurant:
            return None
            
        return {
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
            "customers": [str(customer.restaurant_customer_id) 
                        for customer in restaurant.customers.all()],
        }
            #"employees": [str(employee.restaurant_employee_id) 
            #            for employee in restaurant.employees.all()],