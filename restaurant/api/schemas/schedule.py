from ninja import Schema
from datetime import datetime, time
from typing import Optional
from uuid import UUID

class WorkingHoursSchema(Schema):
    day_of_week: int
    opening_time: time
    closing_time: time
    is_closed: bool = False

class BlockedHoursSchema(Schema):
    start_datetime: datetime
    end_datetime: datetime
    reason: Optional[str] = None

class WorkingHoursResponseSchema(Schema):
    working_hours_id: UUID
    day_of_week: int
    opening_time: time
    closing_time: time
    is_closed: bool

class BlockedHoursResponseSchema(Schema):
    blocked_hours_id: UUID
    start_datetime: datetime
    end_datetime: datetime
    reason: Optional[str]