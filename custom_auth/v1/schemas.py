from ninja import Schema


class RegisterSchema(Schema):
    username: str
    email: str
    password1: str
    password2: str


class LoginSchema(Schema):
    username: str
    password: str


class MessageSchema(Schema):
    message: str


class ProfileSchema(Schema):
    username: str
    email: str


class TokenSchema(Schema):
    access: str
    refresh: str
