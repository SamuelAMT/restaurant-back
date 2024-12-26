from .base import *

DEBUG = False

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

CORS_ALLOWED_ORIGINS = [
    "https://bookabite-restaurante.vercel.app",
]

CSRF_TRUSTED_ORIGINS = [
    "https://bookabite.com.br",
    'https://bookabite-restaurant-back.vercel.app',
    'https://restaurant-back-git-develop-samuel-mirandas-projects.vercel.app',
    'https://bookabite-restaurante.vercel.app',
]