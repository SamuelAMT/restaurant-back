from custom_auth.views import create_user, login, logout, request_password_reset, reset_password, setup_password, change_password
from ninja import Router

auth_router = Router()

auth_router.post("/register/", create_user)
auth_router.post("/login/", login)
auth_router.post("/logout/", logout)
auth_router.post("/password-reset-request/", request_password_reset)
auth_router.post("/password-reset/{uidb64}/{token}/", reset_password)
auth_router.post("/setup-password/{token}/", setup_password)
auth_router.post("/change-password/", change_password)
