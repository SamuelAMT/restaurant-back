from ninja import Schema
from pydantic import EmailStr

class LoginSchema(Schema):
    email: EmailStr
    password: str

class TokenSchema(Schema):
    access: str
    refresh: str
    email: str | None = None
    is_superuser: bool | None = None
    role: str | None = None
    restaurant: dict | None = None
