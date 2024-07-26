from django.urls import path
from .views import register, login_view, logout_view, csrf
from .api import router as auth_router

from ninja import NinjaAPI

api = NinjaAPI()
api.add_router("/auth", auth_router)

urlpatterns = [
    path('csrf/', csrf, name='csrf'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
