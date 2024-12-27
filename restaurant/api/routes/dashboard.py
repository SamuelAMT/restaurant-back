from ninja import Router
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ...services.dashboard_service import DashboardService
from ..schemas.dashboard import DashboardSchema

dashboard_router = Router()

@dashboard_router.get("/{restaurant_id}/dashboard", response=DashboardSchema)
def get_dashboard(request: HttpRequest, restaurant_id: str):
    return DashboardService.get_dashboard_data(restaurant_id)