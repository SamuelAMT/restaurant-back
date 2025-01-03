from ninja import Schema
from pydantic import EmailStr

class ProfileSchema(Schema):
    name: str
    email: EmailStr
    phone: str
    website: str
    description: str
    address: str