from ninja import Schema
from pydantic import EmailStr

class LoginSchema(Schema):
    email: EmailStr
    password: str

class TokenSchema(Schema):
    access: str
    refresh: str

class ErrorSchema(Schema):
    detail: str

class MessageSchema(Schema):
    message: str