from ninja import Schema

class ErrorSchema(Schema):
    detail: str

class MessageSchema(Schema):
    message: str

class RestaurantResponseSchema(Schema):
    restaurant_id: str
    cnpj: str
    name: str
    country_code: str
    phone: str
    email: str
    email_verified: bool
    image: str | None
    website: str
    description: str
    created_at: str
    updated_at: str
    customers: list[str]
    employees: list[str]