from ninja import Schema
from typing import Optional

class SettingsSchema(Schema):
    theme: str
    currency: str
    notification_enabled: bool

class SettingsUpdateSchema(Schema):
    theme: Optional[str] = None
    currency: Optional[str] = None
    notification_enabled: Optional[bool] = None